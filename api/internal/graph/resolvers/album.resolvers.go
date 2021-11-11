package resolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"errors"
	"iris/api/internal/graph/generated"
	"iris/api/internal/models"
	"time"

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

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type albumResolver struct{ *Resolver }
type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
