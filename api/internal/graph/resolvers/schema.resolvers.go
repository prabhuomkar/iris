package resolvers

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"iris/api/internal/graph/generated"
	"iris/api/internal/models"

	"github.com/99designs/gqlgen/graphql"
)

func (r *mediaMetaDataResolver) CreatedAt(ctx context.Context, obj *models.MediaMetaData) (string, error) {
	return "", nil
}

func (r *mutationResolver) Upload(ctx context.Context, file graphql.Upload) (bool, error) {
	return false, nil
}

func (r *mutationResolver) UpdateEntity(ctx context.Context, id string, name string) (bool, error) {
	return false, nil
}

func (r *queryResolver) MediaItem(ctx context.Context, id string) (*models.MediaItem, error) {
	return nil, nil
}

func (r *queryResolver) MediaItems(ctx context.Context, page int, limit int) ([]*models.MediaItem, error) {
	return nil, nil
}

func (r *queryResolver) Search(ctx context.Context, q string) ([]*models.MediaItem, error) {
	return nil, nil
}

func (r *queryResolver) Explore(ctx context.Context) (*models.ExploreResponse, error) {
	return nil, nil
}

func (r *queryResolver) Entity(ctx context.Context, id string) ([]*models.MediaItem, error) {
	return nil, nil
}

// MediaMetaData returns generated.MediaMetaDataResolver implementation.
func (r *Resolver) MediaMetaData() generated.MediaMetaDataResolver { return &mediaMetaDataResolver{r} }

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mediaMetaDataResolver struct{ *Resolver }
type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
