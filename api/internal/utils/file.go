package utils

import (
	"bytes"
	"fmt"
	"image"
	"image/jpeg"
	"log"
	"math"
	"strings"

	"github.com/disintegration/imaging"
	"github.com/gabriel-vasile/mimetype"
	"github.com/linxGnu/goseaweedfs"
	_ "golang.org/x/image/webp" // for image processing
)

const thumbnailSize = 400

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

	// upload thumbnail mediaitem
	var thumbnailURL string
	if canCreateThumbnail(mimeType) {
		src, err := imaging.Decode(bytes.NewReader(fileBytes))
		if err != nil {
			log.Printf("error opening the image for thumbnail generation: %v", err)
			return "", "", err
		}

		var dst *image.NRGBA

		width, height := src.Bounds().Max.X, src.Bounds().Max.Y

		if height > width {
			minHeight := int(math.Min(float64(height), thumbnailSize))
			dst = imaging.Resize(src, 0, minHeight, imaging.NearestNeighbor)
		} else {
			minWidth := int(math.Min(float64(width), thumbnailSize))
			dst = imaging.Resize(src, minWidth, 0, imaging.NearestNeighbor)
		}

		thumbnailBuf := new(bytes.Buffer)

		err = jpeg.Encode(thumbnailBuf, dst, nil)
		if err != nil {
			log.Printf("error encoding created thumbnail: %v", err)
			return "", "", err
		}

		result, err = cdn.Upload(bytes.NewReader(thumbnailBuf.Bytes()), fileName, int64(len(thumbnailBuf.Bytes())), "", "")
		if err != nil {
			return "", "", err
		}

		thumbnailURL = fmt.Sprintf("http://%s/%s", result.Server, result.FileID)
	}

	return sourceURL, thumbnailURL, err
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

func canCreateThumbnail(mimeType string) bool {
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
