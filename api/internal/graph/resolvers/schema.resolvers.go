package resolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"errors"
	"fmt"
	"iris/api/internal/models"
	"iris/api/internal/utils"
	"log"
	"time"

	"github.com/99designs/gqlgen/graphql"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func (r *mutationResolver) Upload(ctx context.Context, file graphql.Upload, albumID *string) (string, error) {
	result, err := r.CDN.Upload(file.File, file.Filename, file.Size, "", "")
	if err != nil {
		log.Printf("some error uploading mediaitems to cdn: %+v", err)

		return "", err
	}

	sourceURL := fmt.Sprintf("http://%s/%s", result.Server, result.FileID)

	insertResult, err := r.DB.Collection(models.ColMediaItems).InsertOne(ctx, bson.D{
		{Key: "sourceUrl", Value: sourceURL},
		{Key: "fileName", Value: file.Filename},
		{Key: "fileSize", Value: file.Size},
		{Key: "mediaMetadata", Value: nil},
		{Key: "createdAt", Value: time.Now()},
		{Key: "updatedAt", Value: time.Now()},
		{Key: "status", Value: StatusUnspecified},
	})
	if err != nil {
		return "", err
	}

	insertedID, ok := insertResult.InsertedID.(primitive.ObjectID)
	if ok {
		go func(insertedID, sourceURL string) {
			message := fmt.Sprintf(
				`{"id":"%s","fileName":"%s","mediaItem":{"downloadUrl":"%s"},"actions":[%s]}`,
				insertedID, file.Filename, sourceURL, r.Config.GetMediaItemFeatures())

			err := r.Queue.Publish([]byte(message))
			if err != nil {
				log.Printf("error publishing event to queue rabbitmq: %+v", err)
			}
		}(insertedID.Hex(), sourceURL)
	} else {
		return "", nil
	}

	if albumID != nil {
		log.Printf("uploaded mediaitem is for album: %s", *albumID)

		albumOID, err := primitive.ObjectIDFromHex(*albumID)
		if err != nil {
			return "", err
		}

		_, err = r.DB.Collection(models.ColAlbums).UpdateByID(ctx, albumOID, bson.D{
			{Key: "$set", Value: bson.D{
				{Key: "$push", Value: bson.D{{Key: "mediaItems", Value: insertedID}}},
			}},
		})
		if err != nil {
			log.Printf("error linking uploaded mediaitem to album: %+v", err)

			return "", err
		}
	}

	return insertedID.Hex(), nil
}

func (r *mutationResolver) Favourite(ctx context.Context, id string, typeArg string) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	if typeArg != actionTypeAdd && typeArg != actionTypeRemove {
		return false, errIncorrectFavouriteActionType
	}

	action := false
	if typeArg == actionTypeAdd {
		action = true
	}

	_, err = r.DB.Collection(models.ColMediaItems).UpdateByID(ctx, oid, bson.D{
		{Key: "$set", Value: bson.D{{Key: "favourite", Value: action}}},
	})
	if err != nil {
		log.Printf("error marking mediaitem as favourite: %+v", err)

		return false, err
	}

	return true, nil
}

func (r *mutationResolver) Delete(ctx context.Context, id string, typeArg string) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	if typeArg != actionTypeAdd && typeArg != actionTypeRemove && typeArg != actionTypePermanent {
		return false, errIncorrectDeleteActionType
	}

	action := false
	if typeArg == actionTypeAdd {
		action = true
	}

	filter := bson.D{{Key: "_id", Value: oid}}
	after := options.After

	result := r.DB.Collection(models.ColMediaItems).FindOneAndUpdate(ctx, filter,
		bson.D{{Key: "$set", Value: bson.D{{Key: "deleted", Value: action}}}},
		&options.FindOneAndUpdateOptions{ReturnDocument: &after},
	)
	if result.Err() != nil {
		log.Printf("error marking mediaitem as deleted: %+v", err)

		return false, result.Err()
	}

	if typeArg == actionTypePermanent {
		var deleteMediaItem *models.MediaItem

		err := result.Decode(&deleteMediaItem)
		if err != nil {
			return false, err
		}

		toUpdateEntities := make([]primitive.ObjectID, len(deleteMediaItem.Entities))

		for idx, entityID := range deleteMediaItem.Entities {
			oEntityID, _ := primitive.ObjectIDFromHex(entityID)
			toUpdateEntities[idx] = oEntityID
		}

		// remove the mediaitem from entities
		_, err = r.DB.Collection(models.ColEntity).UpdateMany(ctx,
			bson.D{{Key: "_id", Value: bson.D{
				{Key: "$in", Value: toUpdateEntities},
			}}},
			bson.D{{Key: "$pull", Value: bson.D{
				{Key: "mediaItems", Value: oid},
			}}},
		)
		if err != nil {
			log.Printf("error deleting entities related to mediaitem: %+v", err)

			return false, err
		}

		// delete from mediaitems collection
		_, err = r.DB.Collection(models.ColMediaItems).DeleteOne(ctx, filter)
		if err != nil {
			log.Printf("error deleting mediaitem: %+v", err)

			return false, err
		}

		utils.DeleteFilesFromCDN(r.CDN, []string{deleteMediaItem.SourceURL, deleteMediaItem.PreviewURL})
	}

	return true, nil
}

func (r *queryResolver) Search(ctx context.Context, q *string, id *string, page *int, limit *int) (*models.MediaItemConnection, error) {
	defaultSearchLimit := 20
	defaultSearchPage := 1

	if limit == nil {
		limit = &defaultSearchLimit
	}

	if page == nil {
		page = &defaultSearchPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	var entityIDs []primitive.ObjectID

	if q != nil {
		cur, err := r.DB.Collection(models.ColEntity).Find(ctx, bson.D{
			{Key: "$text", Value: bson.D{
				{Key: "$search", Value: *q},
				{Key: "$caseSensitive", Value: false},
			}}})
		if err != nil {
			log.Printf("error searching mediaitems: %+v", err)

			return nil, err
		}

		var entities []*models.Entity
		if err = cur.All(ctx, &entities); err != nil {
			return nil, err
		}

		entityIDs = make([]primitive.ObjectID, len(entities))

		for idx, entity := range entities {
			oid, _ := primitive.ObjectIDFromHex(entity.ID)
			entityIDs[idx] = oid
		}
	} else if id != nil {
		entityIDs = make([]primitive.ObjectID, 1)
		oid, _ := primitive.ObjectIDFromHex(*id)
		entityIDs[0] = oid
	}

	colQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{
			{Key: "entities", Value: bson.D{{
				Key: "$in", Value: entityIDs,
			}}}}},
		},
		bson.D{{Key: "$sort", Value: bson.D{{Key: "updatedAt", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{
			{Key: "entities", Value: bson.D{{
				Key: "$in", Value: entityIDs,
			}}}}},
		},
		bson.D{{Key: "$count", Value: "count"}},
	}
	facetStage := bson.D{{
		Key:   "$facet",
		Value: bson.D{{Key: "mediaItems", Value: colQuery}, {Key: "totalCount", Value: cntQuery}},
	}}

	cur, err := r.DB.Collection(models.ColMediaItems).Aggregate(ctx, mongo.Pipeline{facetStage})
	if err != nil {
		return nil, err
	}

	var result []*struct {
		MediaItems []*models.MediaItem `bson:"mediaItems"`
		TotalCount []*struct {
			Count *int `bson:"count"`
		} `bson:"totalCount"`
	}

	if err = cur.All(ctx, &result); err != nil {
		return nil, err
	}

	totalCount := 0
	if len(result) != 0 && len(result[0].TotalCount) != 0 {
		totalCount = *result[0].TotalCount[0].Count
	}

	return &models.MediaItemConnection{
		TotalCount: totalCount,
		Nodes:      result[0].MediaItems,
	}, nil
}

func (r *queryResolver) Autocomplete(ctx context.Context, q string) ([]*models.AutocompleteResponse, error) {
	cur, err := r.DB.Collection(models.ColEntity).Find(ctx, bson.D{
		{Key: "$text", Value: bson.D{
			{Key: "$search", Value: q},
			{Key: "$caseSensitive", Value: false},
		}}})
	if err != nil {
		return nil, err
	}

	var entities []*models.Entity
	if err = cur.All(ctx, &entities); err != nil {
		return nil, err
	}

	matches := make([]*models.AutocompleteResponse, len(entities))
	for idx, entity := range entities {
		matches[idx] = &models.AutocompleteResponse{ID: entity.ID, Name: entity.Name}
	}

	return matches, nil
}

func (r *queryResolver) Favourites(ctx context.Context, page *int, limit *int) (*models.MediaItemConnection, error) {
	defaultFavouritesLimit := 20
	defaultFavouritesPage := 1

	if limit == nil {
		limit = &defaultFavouritesLimit
	}

	if page == nil {
		page = &defaultFavouritesPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	colQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{
			{Key: "$and", Value: bson.A{
				bson.D{{Key: "deleted", Value: bson.D{{Key: "$not", Value: bson.D{{Key: "$eq", Value: true}}}}}},
				bson.D{{Key: "favourite", Value: true}},
			}},
		}}},
		bson.D{{Key: "$sort", Value: bson.D{{Key: "mediaMetadata.creationTime", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{
			{Key: "$and", Value: bson.A{
				bson.D{{Key: "deleted", Value: bson.D{{Key: "$not", Value: bson.D{{Key: "$eq", Value: true}}}}}},
				bson.D{{Key: "favourite", Value: true}},
			}},
		}}},
		bson.D{{Key: "$count", Value: "count"}},
	}
	facetStage := bson.D{{
		Key:   "$facet",
		Value: bson.D{{Key: "mediaItems", Value: colQuery}, {Key: "totalCount", Value: cntQuery}},
	}}

	cur, err := r.DB.Collection(models.ColMediaItems).Aggregate(ctx, mongo.Pipeline{facetStage})
	if err != nil {
		log.Printf("error getting favourite mediaitems: %+v", err)

		return nil, err
	}

	var result []*struct {
		MediaItems []*models.MediaItem `bson:"mediaItems"`
		TotalCount []*struct {
			Count *int `bson:"count"`
		} `bson:"totalCount"`
	}

	if err = cur.All(ctx, &result); err != nil {
		log.Printf("error decoding favourite mediaitems: %+v", err)

		return nil, err
	}

	totalCount := 0
	if len(result) != 0 && len(result[0].TotalCount) != 0 {
		totalCount = *result[0].TotalCount[0].Count
	}

	return &models.MediaItemConnection{
		TotalCount: totalCount,
		Nodes:      result[0].MediaItems,
	}, nil
}

func (r *queryResolver) Deleted(ctx context.Context, page *int, limit *int) (*models.MediaItemConnection, error) {
	defaultDeletedLimit := 20
	defaultDeletedPage := 1

	if limit == nil {
		limit = &defaultDeletedLimit
	}

	if page == nil {
		page = &defaultDeletedPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	colQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{{Key: "deleted", Value: true}}}},
		bson.D{{Key: "$sort", Value: bson.D{{Key: "mediaMetadata.creationTime", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{{Key: "deleted", Value: true}}}},
		bson.D{{Key: "$count", Value: "count"}},
	}
	facetStage := bson.D{{
		Key:   "$facet",
		Value: bson.D{{Key: "mediaItems", Value: colQuery}, {Key: "totalCount", Value: cntQuery}},
	}}
	cur, err := r.DB.Collection(models.ColMediaItems).Aggregate(ctx, mongo.Pipeline{facetStage})

	if err != nil {
		log.Printf("error getting deleted mediaitems: %+v", err)

		return nil, err
	}

	var result []*struct {
		MediaItems []*models.MediaItem `bson:"mediaItems"`
		TotalCount []*struct {
			Count *int `bson:"count"`
		} `bson:"totalCount"`
	}

	if err = cur.All(ctx, &result); err != nil {
		log.Printf("error decoding deleted mediaitems: %+v", err)

		return nil, err
	}

	totalCount := 0
	if len(result) != 0 && len(result[0].TotalCount) != 0 {
		totalCount = *result[0].TotalCount[0].Count
	}

	return &models.MediaItemConnection{
		TotalCount: totalCount,
		Nodes:      result[0].MediaItems,
	}, nil
}

// !!! WARNING !!!
// The code below was going to be deleted when updating resolvers. It has been copied here so you have
// one last chance to move it out of harms way if you want. There are two reasons this happens:
//  - When renaming or deleting a resolver the old code will be put in here. You can safely delete
//    it when you're done.
//  - You have helper methods in this file. Move them out to keep these resolver files clean.
const (
	StatusUnspecified = "UNSPECIFIED"
	StatusProcessing  = "PROCESSING"
	StatusReady       = "READY"
	StatusFailed      = "FAILED"
)

var (
	errIncorrectFavouriteActionType = errors.New("incorrect action type for favourite")
	errIncorrectDeleteActionType    = errors.New("incorrect action type for delete")
)

const (
	actionTypeAdd       = "add"
	actionTypeRemove    = "remove"
	actionTypePermanent = "permanent"
)
