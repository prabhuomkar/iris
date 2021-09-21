package utils

import (
	"context"
	"iris/api/internal/models"
	"iris/api/pkg/mongo"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	defaultEntityListItemLimit int64
)

// Returns list of entities based on entity type
func GetEntitiesByType(ctx context.Context, db *mongo.Connection, entityType string) ([]*models.Entity, error) {
	defaultEntityListItemLimit = 10

	cur, err := db.Collection(models.ColEntity).Find(ctx,
		bson.D{{Key: "entityType", Value: entityType}}, &options.FindOptions{Limit: &defaultEntityListItemLimit})
	if err != nil {
		return nil, err
	}

	var result []*models.Entity
	if err = cur.All(ctx, &result); err != nil {
		return nil, err
	}

	return result, nil
}
