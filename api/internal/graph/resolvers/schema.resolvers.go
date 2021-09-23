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
		go func(insertedID, imageURL string) {
			err := r.Queue.Publish([]byte(fmt.Sprintf(`{"id":"%s","imageUrl":"%s"}`, insertedID, imageURL)))
			if err != nil {
				log.Printf("error while publishing event to rabbitmq: %v", err)
			} else {
				log.Printf("published event to rabbitmq for image: %s", imageURL)
			}
		}(insertedID.Hex(), imageURL)
	} else {
		return false, nil
	}

	return true, nil
}

func (r *mutationResolver) UpdateEntity(ctx context.Context, id string, name string) (bool, error) {
	return false, nil
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

func (r *queryResolver) Search(ctx context.Context, q string, page *int, limit *int) (*models.MediaItemConnection, error) {
	return nil, nil
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

func (r *queryResolver) Entity(ctx context.Context, id string, page *int, limit *int) (*models.MediaItemConnection, error) {
	return nil, nil
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
