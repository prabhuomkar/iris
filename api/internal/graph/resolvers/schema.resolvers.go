package resolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"errors"
	"fmt"
	"iris/api/internal/graph/generated"
	"iris/api/internal/models"
	"iris/api/internal/utils"
	"log"
	"time"

	"github.com/99designs/gqlgen/graphql"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

func (r *albumResolver) MediaItems(ctx context.Context, obj *models.Album, page *int, limit *int) (*models.MediaItemConnection, error) {
	defaultAlbumMediaItemsLimit := 20
	defaultAlbumMediaItemsPage := 1

	if limit == nil {
		limit = &defaultAlbumMediaItemsLimit
	}

	if page == nil {
		page = &defaultAlbumMediaItemsPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	albumID, _ := primitive.ObjectIDFromHex(obj.ID)

	lookupStage := bson.D{{Key: "$match", Value: bson.D{
		{Key: "_id", Value: albumID},
	}}}
	matchStage := bson.D{{Key: "$lookup", Value: bson.D{
		{Key: "from", Value: "mediaitems"},
		{Key: "localField", Value: "mediaItems"},
		{Key: "foreignField", Value: "_id"},
		{Key: "as", Value: "mediaItem"},
	}}}

	cur, err := r.DB.Collection(models.ColAlbums).Aggregate(ctx, mongo.Pipeline{
		matchStage,
		lookupStage,
		bson.D{{Key: "$unwind", Value: "$mediaItem"}},
		bson.D{{Key: "$sort", Value: bson.D{{Key: "mediaItem.mediaMetadata.creationTime", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	})
	if err != nil {
		return nil, err
	}

	var results []*models.MediaItem
	for cur.Next(ctx) {
		var result *struct {
			MediaItem *models.MediaItem `bson:"mediaItem"`
		}

		if err := cur.Decode(&result); err != nil {
			return nil, err
		}

		results = append(results, result.MediaItem)
	}

	totalCount := len(obj.MediaItems)

	return &models.MediaItemConnection{
		TotalCount: totalCount,
		Nodes:      results,
	}, nil
}

func (r *entityResolver) MediaItems(ctx context.Context, obj *models.Entity, page *int, limit *int) (*models.MediaItemConnection, error) {
	defaultEntityMediaItemsLimit := 20
	defaultEntityMediaItemsPage := 1

	if limit == nil {
		limit = &defaultEntityMediaItemsLimit
	}

	if page == nil {
		page = &defaultEntityMediaItemsPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	entityID, _ := primitive.ObjectIDFromHex(obj.ID)

	colQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{
			{Key: "entities", Value: bson.D{{Key: "$in", Value: bson.A{entityID}}}},
		}}},
		bson.D{{Key: "$sort", Value: bson.D{{Key: "mediaMetadata.creationTime", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{
			{Key: "entities", Value: bson.D{{Key: "$in", Value: bson.A{entityID}}}},
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

func (r *mediaItemResolver) Entities(ctx context.Context, obj *models.MediaItem) ([]*models.Entity, error) {
	entityIDs := make([]primitive.ObjectID, len(obj.Entities))

	for idx, strID := range obj.Entities {
		oid, _ := primitive.ObjectIDFromHex(strID)
		entityIDs[idx] = oid
	}

	cur, err := r.DB.Collection(models.ColEntity).Find(ctx, bson.M{"_id": bson.M{"$in": entityIDs}})
	if err != nil {
		return nil, err
	}

	var result []*models.Entity
	if err = cur.All(ctx, &result); err != nil {
		return nil, err
	}

	return result, nil
}

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

func (r *mutationResolver) UpdateEntity(ctx context.Context, id string, name string) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	res := r.DB.Collection(models.ColEntity).FindOneAndUpdate(ctx, bson.D{
		{Key: "_id", Value: oid}, {Key: "entityType", Value: "people"},
	}, bson.D{{Key: "$set", Value: bson.D{{Key: "name", Value: name}}}})
	if res.Err() != nil {
		return false, res.Err()
	}

	return true, nil
}

func (r *mutationResolver) UpdateFavourite(ctx context.Context, id string, typeArg string) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	if typeArg != "add" && typeArg != "remove" {
		return false, errIncorrectFavouriteActionType
	}

	action := false
	if typeArg == "add" {
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

func (r *mutationResolver) UpdateDescription(ctx context.Context, id string, description string) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	_, err = r.DB.Collection(models.ColMediaItems).UpdateByID(ctx, oid, bson.D{
		{Key: "$set", Value: bson.D{{Key: "description", Value: description}}},
	})
	if err != nil {
		return false, err
	}

	return true, nil
}

func (r *mutationResolver) CreateAlbum(ctx context.Context, input models.CreateAlbumInput) (bool, error) {
	mediaItems := make([]primitive.ObjectID, len(input.MediaItems))
	for idx, mediaItem := range input.MediaItems {
		oid, _ := primitive.ObjectIDFromHex(*mediaItem)
		mediaItems[idx] = oid
	}

	_, err := r.DB.Collection(models.ColAlbums).InsertOne(ctx, bson.D{
		{Key: "name", Value: input.Name},
		{Key: "description", Value: input.Description},
		{Key: "mediaItems", Value: mediaItems},
		{Key: "createdAt", Value: time.Now()},
		{Key: "updatedAt", Value: time.Now()},
	})
	if err != nil {
		return false, err
	}

	return true, nil
}

func (r *mutationResolver) UpdateAlbum(ctx context.Context, id string, input models.UpdateAlbumInput) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	_, err = r.DB.Collection(models.ColAlbums).UpdateByID(ctx, oid, bson.D{{
		Key: "$set", Value: bson.D{
			{Key: "name", Value: input.Name},
			{Key: "description", Value: input.Description},
			{Key: "updatedAt", Value: time.Now()},
		}}})
	if err != nil {
		return false, err
	}

	return true, nil
}

func (r *mutationResolver) DeleteAlbum(ctx context.Context, id string) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	_, err = r.DB.Collection(models.ColAlbums).DeleteOne(ctx, bson.D{{Key: "_id", Value: oid}})
	if err != nil {
		return false, err
	}

	return true, nil
}

func (r *queryResolver) MediaItem(ctx context.Context, id string) (*models.MediaItem, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return nil, err
	}

	filter := bson.D{{Key: "_id", Value: oid}}

	var result *models.MediaItem

	err = r.DB.Collection(models.ColMediaItems).FindOne(ctx, filter).Decode(&result)
	if err != nil {
		if errors.Is(err, mongo.ErrNoDocuments) {
			return nil, err
		}

		return nil, err
	}

	return result, err
}

func (r *queryResolver) MediaItems(ctx context.Context, page *int, limit *int) (*models.MediaItemConnection, error) {
	defaultMediaItemsLimit := 20
	defaultMediaItemsPage := 1

	if limit == nil {
		limit = &defaultMediaItemsLimit
	}

	if page == nil {
		page = &defaultMediaItemsPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	colQuery := bson.A{
		bson.D{{Key: "$sort", Value: bson.D{{Key: "mediaMetadata.creationTime", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{bson.D{{Key: "$count", Value: "count"}}}
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

func (r *queryResolver) Explore(ctx context.Context) (*models.ExploreResponse, error) {
	// later(omkar): move entityType to enums
	people, err := utils.GetEntitiesByType(ctx, r.DB, "people")
	if err != nil {
		return nil, err
	}

	places, err := utils.GetEntitiesByType(ctx, r.DB, "places")
	if err != nil {
		return nil, err
	}

	things, err := utils.GetEntitiesByType(ctx, r.DB, "things")
	if err != nil {
		return nil, err
	}

	return &models.ExploreResponse{
		People: people, Places: places, Things: things,
	}, nil
}

func (r *queryResolver) Entities(ctx context.Context, entityType string, page *int, limit *int) (*models.EntityItemConnection, error) {
	defaultEnitiesLimit := 20
	defaultEnitiesPage := 1

	if limit == nil {
		limit = &defaultEnitiesLimit
	}

	if page == nil {
		page = &defaultEnitiesPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	colQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{{Key: "entityType", Value: entityType}}}},
		bson.D{{Key: "$sort", Value: bson.D{{Key: "updatedAt", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{{Key: "entityType", Value: entityType}}}},
		bson.D{{Key: "$count", Value: "count"}},
	}
	facetStage := bson.D{{
		Key:   "$facet",
		Value: bson.D{{Key: "entities", Value: colQuery}, {Key: "totalCount", Value: cntQuery}},
	}}

	cur, err := r.DB.Collection(models.ColEntity).Aggregate(ctx, mongo.Pipeline{facetStage})
	if err != nil {
		return nil, err
	}

	var result []*struct {
		Entities   []*models.Entity `bson:"entities"`
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

	return &models.EntityItemConnection{
		TotalCount: totalCount,
		Nodes:      result[0].Entities,
	}, nil
}

func (r *queryResolver) Entity(ctx context.Context, id string) (*models.Entity, error) {
	entityID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return nil, err
	}

	var entity models.Entity

	err = r.DB.Collection(models.ColEntity).FindOne(ctx, bson.D{{Key: "_id", Value: entityID}}).Decode(&entity)
	if err != nil {
		return nil, err
	}

	return &entity, nil
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
		bson.D{{Key: "$match", Value: bson.D{{Key: "favourite", Value: true}}}},
		bson.D{{Key: "$sort", Value: bson.D{{Key: "mediaMetadata.creationTime", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{
		bson.D{{Key: "$match", Value: bson.D{{Key: "favourite", Value: true}}}},
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

func (r *queryResolver) Album(ctx context.Context, id string) (*models.Album, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return nil, err
	}

	filter := bson.D{{Key: "_id", Value: oid}}

	var result *models.Album

	err = r.DB.Collection(models.ColAlbums).FindOne(ctx, filter).Decode(&result)
	if err != nil {
		if errors.Is(err, mongo.ErrNoDocuments) {
			return nil, err
		}

		return nil, err
	}

	return result, err
}

func (r *queryResolver) Albums(ctx context.Context, page *int, limit *int) (*models.AlbumConnection, error) {
	defaultAlbumsLimit := 20
	defaultAlbumsPage := 1

	if limit == nil {
		limit = &defaultAlbumsLimit
	}

	if page == nil {
		page = &defaultAlbumsPage
	}

	skip := int64(*limit * (*page - 1))
	itemsPerPage := int64(*limit)

	colQuery := bson.A{
		bson.D{{Key: "$sort", Value: bson.D{{Key: "updatedAt", Value: -1}}}},
		bson.D{{Key: "$skip", Value: skip}},
		bson.D{{Key: "$limit", Value: itemsPerPage}},
	}
	cntQuery := bson.A{bson.D{{Key: "$count", Value: "count"}}}
	facetStage := bson.D{{
		Key:   "$facet",
		Value: bson.D{{Key: "albums", Value: colQuery}, {Key: "totalCount", Value: cntQuery}},
	}}

	cur, err := r.DB.Collection(models.ColAlbums).Aggregate(ctx, mongo.Pipeline{facetStage})
	if err != nil {
		return nil, err
	}

	var result []*struct {
		Albums     []*models.Album `bson:"albums"`
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

	return &models.AlbumConnection{
		TotalCount: totalCount,
		Nodes:      result[0].Albums,
	}, nil
}

// Album returns generated.AlbumResolver implementation.
func (r *Resolver) Album() generated.AlbumResolver { return &albumResolver{r} }

// Entity returns generated.EntityResolver implementation.
func (r *Resolver) Entity() generated.EntityResolver { return &entityResolver{r} }

// MediaItem returns generated.MediaItemResolver implementation.
func (r *Resolver) MediaItem() generated.MediaItemResolver { return &mediaItemResolver{r} }

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type albumResolver struct{ *Resolver }
type entityResolver struct{ *Resolver }
type mediaItemResolver struct{ *Resolver }
type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }

// !!! WARNING !!!
// The code below was going to be deleted when updating resolvers. It has been copied here so you have
// one last chance to move it out of harms way if you want. There are two reasons this happens:
//  - When renaming or deleting a resolver the old code will be put in here. You can safely delete
//    it when you're done.
//  - You have helper methods in this file. Move them out to keep these resolver files clean.
var errIncorrectFavouriteActionType = errors.New("incorrect action type for favourite")
