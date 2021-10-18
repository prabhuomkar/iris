package models

const ColEntity = "entities"

type Entity struct {
	ID         string   `json:"id" bson:"_id"`
	Name       string   `json:"name"`
	ImageURL   string   `json:"imageUrl"`
	EntityType string   `json:"entityType"`
	MediaItems []string `json:"mediaItems"`
	CreatedAt  string   `json:"createdAt"`
	UpdatedAt  string   `json:"updatedAt"`
}
