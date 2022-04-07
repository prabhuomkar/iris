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

	matchStage := bson.D{{Key: "$match", Value: bson.D{
		{Key: "_id", Value: albumID},
	}}}
	lookupStage := bson.D{{Key: "$lookup", Value: bson.D{
		{Key: "from", Value: "mediaitems"},
		{Key: "let", Value: bson.D{
			{Key: "mediaItems", Value: "$mediaItems"},
		}},
		{Key: "pipeline", Value: bson.A{
			bson.D{{Key: "$match", Value: bson.D{
				{Key: "$expr", Value: bson.D{{Key: "$and", Value: bson.A{
					bson.D{{Key: "$ne", Value: bson.A{"$deleted", true}}},
					bson.D{{Key: "$in", Value: bson.A{"$_id", "$$mediaItems"}}},
				}}}},
			}}},
		}},
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

	totalCount := len(results)

	return &models.MediaItemConnection{
		TotalCount: totalCount,
		Nodes:      results,
	}, nil
}

func (r *mutationResolver) CreateAlbum(ctx context.Context, input models.CreateAlbumInput) (*string, error) {
	mediaItems := make([]primitive.ObjectID, len(input.MediaItems))

	for idx, mediaItem := range input.MediaItems {
		oid, _ := primitive.ObjectIDFromHex(*mediaItem)
		mediaItems[idx] = oid
	}

	if len(mediaItems) == 0 {
		return nil, errInvalidMediaItemsForAlbum
	}

	var thumbnailMediaItem models.MediaItem

	err := r.DB.Collection(models.ColMediaItems).FindOne(ctx, bson.D{{Key: "_id", Value: mediaItems[0]}}).Decode(&thumbnailMediaItem)
	if err != nil {
		return nil, err
	}

	result, err := r.DB.Collection(models.ColAlbums).InsertOne(ctx, bson.D{
		{Key: "name", Value: input.Name},
		{Key: "description", Value: input.Description},
		{Key: "thumbnailUrl", Value: thumbnailMediaItem.ThumbnailURL},
		{Key: "mediaItems", Value: mediaItems},
		{Key: "createdAt", Value: time.Now()},
		{Key: "updatedAt", Value: time.Now()},
	})
	if err != nil {
		return nil, err
	}

	var albumID string

	albumOID, ok := result.InsertedID.(primitive.ObjectID)
	if ok {
		albumID = albumOID.Hex()
	}

	return &albumID, nil
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

func (r *mutationResolver) UpdateAlbumThumbnailURL(ctx context.Context, id string, mediaItemID string) (bool, error) {
	oid, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	mediaItemOID, err := primitive.ObjectIDFromHex(mediaItemID)
	if err != nil {
		return false, err
	}

	var mediaItem models.MediaItem

	err = r.DB.Collection(models.ColMediaItems).FindOne(ctx, bson.D{{Key: "_id", Value: mediaItemOID}}).Decode(&mediaItem)
	if err != nil {
		return false, err
	}

	_, err = r.DB.Collection(models.ColAlbums).UpdateByID(ctx, oid, bson.D{
		{Key: "$set", Value: bson.D{
			{Key: "thumbnailUrl", Value: mediaItem.ThumbnailURL},
		}},
	})
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

func (r *mutationResolver) UpdateAlbumMediaItems(ctx context.Context, id string, typeArg string, mediaItems []string) (bool, error) {
	albumID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return false, err
	}

	mediaItemIDs := []primitive.ObjectID{}

	for _, mediaItem := range mediaItems {
		oid, err := primitive.ObjectIDFromHex(mediaItem)
		if err != nil {
			return false, err
		}

		mediaItemIDs = append(mediaItemIDs, oid)
	}

	if typeArg != actionTypeAdd && typeArg != actionTypeRemove {
		return false, errIncorrectUpdateAlbumMediaItemsActionType
	}

	update := bson.D{{Key: "$pull", Value: bson.D{{Key: "mediaItems", Value: bson.D{{Key: "$in", Value: mediaItemIDs}}}}}}
	if typeArg == actionTypeAdd {
		update = bson.D{{Key: "$addToSet", Value: bson.D{{Key: "mediaItems", Value: bson.D{{Key: "$each", Value: mediaItemIDs}}}}}}
	}

	filter := bson.D{{Key: "_id", Value: albumID}}

	_, err = r.DB.Collection(models.ColAlbums).UpdateOne(ctx, filter, update)
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

// !!! WARNING !!!
// The code below was going to be deleted when updating resolvers. It has been copied here so you have
// one last chance to move it out of harms way if you want. There are two reasons this happens:
//  - When renaming or deleting a resolver the old code will be put in here. You can safely delete
//    it when you're done.
//  - You have helper methods in this file. Move them out to keep these resolver files clean.
var errInvalidMediaItemsForAlbum = errors.New("invalid number of media items for album")
var errIncorrectUpdateAlbumMediaItemsActionType = errors.New("incorrect action type for updating album mediaItems")
