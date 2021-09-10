package models

import (
	database "iris/api/pkg/mongo"

	"go.mongodb.org/mongo-driver/mongo"
)

const collectionEntity = "entities"

type Entity struct {
	ID         string `json:"id" bson:"_id"`
	Name       string `json:"name"`
	ImageURL   string `json:"imageUrl"`
	EntityType string `json:"entityType"`
	CreatedAt  string `json:"createdAt"`
	UpdatedAt  string `json:"updatedAt"`
}

func Entities(db *database.Connection) *mongo.Collection {
	return db.Collection(collectionEntity)
}
