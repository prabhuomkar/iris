package utils

import (
	"bytes"
	"fmt"
	"log"
	"strings"

	"github.com/gabriel-vasile/mimetype"
	"github.com/linxGnu/goseaweedfs"
)

func UploadFilesToCDN(cdn *goseaweedfs.Seaweed, mimeType, fileName string, fileSize int64, fileBytes []byte) (string, string, error) {
	// upload source mediaitem
	result, err := cdn.Upload(bytes.NewReader(fileBytes), fileName, fileSize, "", "")
	if err != nil {
		return "", "", err
	}

	sourceURL := fmt.Sprintf("http://%s/%s", result.Server, result.FileID)

	// upload previewMediaItem mediaitem
	var previewURL string
	// nolint
	if CanFileHavePreviewMediaItem(mimeType) {
		previewMediaItemBuf, err := GetPreviewFile(fileBytes)
		if err != nil {
			return "", "", err
		}

		result, err = cdn.Upload(bytes.NewReader(previewMediaItemBuf.Bytes()),
			GetPreviewFileName(fileName), int64(len(previewMediaItemBuf.Bytes())), "", "")
		if err != nil {
			return "", "", err
		}

		previewURL = fmt.Sprintf("http://%s/%s", result.Server, result.FileID)
	}

	return sourceURL, previewURL, err
}

func DeleteFilesFromCDN(cdn *goseaweedfs.Seaweed, imageURLs []string) {
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

func GetFileMimeType(input []byte) string {
	mimeType := mimetype.Detect(input)

	return mimeType.String()
}

func CanFileHavePreviewMediaItem(mimeType string) bool {
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
