package models

const ColEntity = "entities"

type Entity struct {
	ID           string   `json:"id" bson:"_id"`
	Name         string   `json:"name"`
	EntityType   string   `json:"entityType"`
	ThumbnailURL string   `json:"thumbnailUrl"`
	MediaItems   []string `json:"mediaItems"`
	CreatedAt    string   `json:"createdAt"`
	UpdatedAt    string   `json:"updatedAt"`
}
