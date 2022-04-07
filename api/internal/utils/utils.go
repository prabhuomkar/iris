package utils

import (
	"bytes"
	"io"
	"log"
	"strings"

	"github.com/gabriel-vasile/mimetype"
	"github.com/linxGnu/goseaweedfs"
)

func GetMimeType(input io.Reader) (string, io.Reader, error) {
	header := bytes.NewBuffer(nil)
	mimeType, err := mimetype.DetectReader(io.TeeReader(input, header))
	recycled := io.MultiReader(header, input)

	if err != nil {
		return "", recycled, err
	}

	return mimeType.String(), recycled, err
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
