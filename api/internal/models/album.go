package models

import "time"

const ColAlbums = "albums"

type (
	Album struct {
		ID           string    `json:"id" bson:"_id"`
		Name         string    `json:"name"`
		Description  string    `json:"description"`
		ThumbnailURL string    `json:"thumbnailUrl"`
		MediaItems   []string  `json:"mediaItems"`
		CreatedAt    time.Time `json:"createdAt"`
		UpdatedAt    time.Time `json:"updatedAt"`
	}
)
