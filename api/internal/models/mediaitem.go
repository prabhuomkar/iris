package models

const ColMediaItems = "mediaitems"

type (
	MediaItem struct {
		ID            string         `json:"id" bson:"_id"`
		Description   string         `json:"description"`
		ImageURL      string         `json:"imageUrl"`
		MimeType      string         `json:"mimeType"`
		FileName      string         `json:"fileName"`
		MediaMetadata *MediaMetaData `json:"mediaMetadata"`
		CreatedAt     string         `json:"createdAt"`
		UpdatedAt     string         `json:"updatedAt"`
	}

	MediaMetaData struct {
		CreationTime string `json:"creationTime"`
		Width        int    `json:"width"`
		Height       int    `json:"height"`
		Photo        *Photo `json:"photo"`
	}

	Photo struct {
		CameraMake      *string  `json:"cameraMake"`
		CameraModel     *string  `json:"cameraModel"`
		FocalLength     *int     `json:"focalLength"`
		ApertureFNumber *float64 `json:"apertureFNumber"`
		IsoEquivalent   *int     `json:"isoEquivalent"`
		ExposureTime    *string  `json:"exposureTime"`
	}
)
