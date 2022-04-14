package models

import "time"

const ColMediaItems = "mediaitems"

type (
	MediaItem struct {
		ID                string         `json:"id" bson:"_id"`
		Description       string         `json:"description"`
		PreviewURL        string         `json:"previewUrl"`
		SourceURL         string         `json:"sourceUrl"`
		MimeType          string         `json:"mimeType"`
		FileName          string         `json:"fileName"`
		FileSize          int64          `json:"fileSize"`
		MediaMetadata     *MediaMetaData `json:"mediaMetadata"`
		ContentCategories []string       `json:"contentCategories"`
		Entities          []string       `json:"entities"`
		Albums            []string       `json:"albums"`
		Favourite         bool           `json:"favourite"`
		Deleted           bool           `json:"deleted"`
		CreatedAt         time.Time      `json:"createdAt"`
		UpdatedAt         time.Time      `json:"updatedAt"`
		Status            string         `json:"status"`
	}

	MediaMetaData struct {
		CreationTime time.Time `json:"creationTime"`
		Width        *int      `json:"width"`
		Height       *int      `json:"height"`
		Photo        *Photo    `json:"photo"`
		Video        *Video    `json:"video"`
		Location     *Location `json:"location"`
	}

	Photo struct {
		CameraMake      *string  `json:"cameraMake"`
		CameraModel     *string  `json:"cameraModel"`
		FocalLength     *float64 `json:"focalLength"`
		ApertureFNumber *float64 `json:"apertureFNumber"`
		IsoEquivalent   *int     `json:"isoEquivalent"`
		ExposureTime    *float64 `json:"exposureTime"`
	}

	Video struct {
		CameraMake  *string `json:"cameraMake"`
		CameraModel *string `json:"cameraModel"`
		Fps         *int    `json:"fps"`
		Status      *string `json:"status"`
	}

	Location struct {
		Latitude  *float64 `json:"latitude"`
		Longitude *float64 `json:"longitude"`
	}
)
