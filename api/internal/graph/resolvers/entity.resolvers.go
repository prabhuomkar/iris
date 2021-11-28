package resolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"iris/api/internal/graph/generated"
	"iris/api/internal/models"
	"iris/api/internal/utils"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

func (r *entityResolver) DisplayMediaItem(ctx context.Context, obj *models.Entity) (*models.MediaItem, error) {
	mediaItemID, err := primitive.ObjectIDFromHex(obj.MediaItems[0])
	if err != nil {
		return nil, err
	}

	filter := bson.D{{Key: "_id", Value: mediaItemID}}

	var result *models.MediaItem

	err = r.DB.Collection(models.ColMediaItems).FindOne(ctx, filter).Decode(&result)
	if err != nil {
		return nil, err
	}

	return result, nil
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
			{Key: "$and", Value: bson.A{
				bson.D{{Key: "deleted", Value: bson.D{{Key: "$not", Value: bson.D{{Key: "$eq", Value: true}}}}}},
				bson.D{{Key: "entities", Value: bson.D{{Key: "$in", Value: bson.A{entityID}}}}},
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
				bson.D{{Key: "entities", Value: bson.D{{Key: "$in", Value: bson.A{entityID}}}}},
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

// Entity returns generated.EntityResolver implementation.
func (r *Resolver) Entity() generated.EntityResolver { return &entityResolver{r} }

type entityResolver struct{ *Resolver }
