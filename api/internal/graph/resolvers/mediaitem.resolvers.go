package resolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"errors"
	"iris/api/internal/graph/generated"
	"iris/api/internal/models"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

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

// MediaItem returns generated.MediaItemResolver implementation.
func (r *Resolver) MediaItem() generated.MediaItemResolver { return &mediaItemResolver{r} }

type mediaItemResolver struct{ *Resolver }
