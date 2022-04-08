package utils

import (
	"bytes"
	"fmt"
	"image"
	"image/jpeg"
	"log"
	"strings"

	"github.com/disintegration/imaging"
	"github.com/gabriel-vasile/mimetype"
	"github.com/linxGnu/goseaweedfs"
	_ "golang.org/x/image/webp" // for image processing
)

func GetMimeType(input []byte) string {
	mimeType := mimetype.Detect(input)
	return mimeType.String()
}

func UploadImagesToCDN(cdn *goseaweedfs.Seaweed, mimeType, fileName string, fileSize int64, fileBytes []byte) (string, string, error) {
	// upload source mediaitem
	result, err := cdn.Upload(bytes.NewReader(fileBytes), fileName, fileSize, "", "")
	if err != nil {
		return "", "", err
	}

	sourceURL := fmt.Sprintf("http://%s/%s", result.Server, result.FileID)

	// upload previewMediaItem mediaitem
	var previewURL string
	if canCreatepreviewMediaItem(mimeType) {
		src, err := imaging.Decode(bytes.NewReader(fileBytes))
		if err != nil {
			log.Printf("error opening the image for previewMediaItem generation: %v", err)
			return "", "", err
		}

		var dst *image.NRGBA

		width, height := src.Bounds().Max.X, src.Bounds().Max.Y

		if height > width {
			dst = imaging.Resize(src, 0, height, imaging.NearestNeighbor)
		} else {
			dst = imaging.Resize(src, width, 0, imaging.NearestNeighbor)
		}

		previewMediaItemBuf := new(bytes.Buffer)

		err = jpeg.Encode(previewMediaItemBuf, dst, nil)
		if err != nil {
			log.Printf("error encoding created previewMediaItem: %v", err)
			return "", "", err
		}

		result, err = cdn.Upload(bytes.NewReader(previewMediaItemBuf.Bytes()), fileName, int64(len(previewMediaItemBuf.Bytes())), "", "")
		if err != nil {
			return "", "", err
		}

		previewURL = fmt.Sprintf("http://%s/%s", result.Server, result.FileID)
	}

	return sourceURL, previewURL, err
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

func canCreatepreviewMediaItem(mimeType string) bool {
	canConvertMimeTypes := []string{
		"image/jpeg", "image/png", "image/webp", "image/bmp", "image/gif", "image/tiff",
	}

	for _, canConvertMimeType := range canConvertMimeTypes {
		if canConvertMimeType == mimeType {
			return true
		}
	}

	return false
}
