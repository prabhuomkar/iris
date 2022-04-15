package utils

import (
	"log"
	"strings"

	"github.com/linxGnu/goseaweedfs"
)

func DeleteFilesFromCDN(cdn *goseaweedfs.Seaweed, imageURLs []string) {
	for _, imageURL := range imageURLs {
		if len(imageURL) > 0 {
			splits := strings.Split(imageURL, "/")
			fileID := splits[len(splits)-1]

			err := cdn.DeleteFile(fileID, nil)
			if err != nil {
				log.Printf("error deleting images from cdn: %+v", err)
			}
		}
	}
}
