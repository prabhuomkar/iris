package utils

import (
	"bytes"
	"fmt"
	"image"
	"image/jpeg"
	"log"
	"path/filepath"

	"github.com/disintegration/imaging"
	_ "golang.org/x/image/webp" // for image processing
)

func GetPreviewFile(fileBytes []byte) (*bytes.Buffer, error) {
	src, err := imaging.Decode(bytes.NewReader(fileBytes))
	if err != nil {
		log.Printf("error opening the image for previewMediaItem generation: %v", err)

		return nil, err
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

		return nil, err
	}

	return previewMediaItemBuf, err
}

func GetPreviewFileName(fileName string) string {
	extension := filepath.Ext(fileName)

	if len(extension) > 1 {
		return fmt.Sprintf("%s.jpg", fileName[:(len(fileName)-len(extension))])
	}

	return fmt.Sprintf("%s.jpg", fileName)
}
