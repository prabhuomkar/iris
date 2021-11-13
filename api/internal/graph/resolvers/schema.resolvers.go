package resolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"errors"
	"fmt"
	"iris/api/internal/models"
	"log"
	"time"

	"github.com/99designs/gqlgen/graphql"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
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

func (r *mutationResolver) Upload(ctx context.Context, file graphql.Upload) (bool, error) {
	result, err := r.CDN.Upload(file.File, file.Filename, file.Size, "", "")
	if err != nil {
		return false, err
	}

	imageURL := fmt.Sprintf("http://%s/%s", result.Server, result.FileID)

	insertResult, err := r.DB.Collection(models.ColMediaItems).InsertOne(ctx, bson.D{
		{Key: "imageUrl", Value: imageURL},
		{Key: "description", Value: nil},
		{Key: "mimeType", Value: result.MimeType},
		{Key: "fileName", Value: result.FileName},
		{Key: "fileSize", Value: result.FileSize},
		{Key: "mediaMetadata", Value: nil},
		{Key: "createdAt", Value: time.Now()},
		{Key: "updatedAt", Value: time.Now()},
	})
	if err != nil {
		return false, err
	}

	insertedID, ok := insertResult.InsertedID.(primitive.ObjectID)
	if ok {
		go func(insertedID, imageURL, mimeType string) {
			err := r.Queue.Publish([]byte(fmt.Sprintf(`{"id":"%s","imageUrl":"%s","mimeType":"%s"}`, insertedID, imageURL, mimeType)))
			if err != nil {
				log.Printf("error while publishing event to rabbitmq: %v", err)
			} else {
				log.Printf("published event to rabbitmq for image: %s mimeType: %s", imageURL, mimeType)
			}
		}(insertedID.Hex(), imageURL, result.MimeType)
	} else {
		return false, nil
	}

	return true, nil
}

func (r *mutationResolver) UpdateFavourite(ctx context.Context, id string, typeArg string) (bool, error) {
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

	if typeArg != "permanent" {
		action := false
		if typeArg == actionTypeAdd {
			action = true
		}

		_, err = r.DB.Collection(models.ColMediaItems).UpdateByID(ctx, oid, bson.D{
			{Key: "$set", Value: bson.D{{Key: "deleted", Value: action}}},
		})
		if err != nil {
			return false, err
		}

		return true, nil
	}

	// FOR(omkar): handle complex operations for permanent delete here
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
