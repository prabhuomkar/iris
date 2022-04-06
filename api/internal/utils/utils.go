package utils

import (
	"github.com/99designs/gqlgen/graphql"
	"github.com/gabriel-vasile/mimetype"
)

func GetMimeType(file graphql.Upload) (string, error) {
	mtype, err := mimetype.DetectReader(file.File)
	if err != nil {
		return "", err
	}

	return mtype.String(), nil
}
