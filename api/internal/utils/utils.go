package utils

import (
	"log"
	"strings"

	"github.com/99designs/gqlgen/graphql"
	"github.com/gabriel-vasile/mimetype"
	"github.com/linxGnu/goseaweedfs"
)

func GetMimeType(file graphql.Upload) (string, error) {
	mtype, err := mimetype.DetectReader(file.File)
	if err != nil {
		return "", err
	}

	return mtype.String(), nil
}

func DeleteImagesFromCDN(cdn *goseaweedfs.Seaweed, imageURLs []string) {
	for _, imageURL := range imageURLs {
		if len(imageURL) > 0 {
			splits := strings.Split(imageURL, "/")
			fileID := splits[len(splits)-1]

			err := cdn.DeleteFile(fileID, nil)
			if err != nil {
				log.Printf("error deleting images from cdn: %v", err)
			}
		}
	}
}
