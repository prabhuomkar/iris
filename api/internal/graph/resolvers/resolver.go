package resolvers

import (
	"iris/api/internal/config"
	"iris/api/pkg/mongo"
	"iris/api/pkg/rabbitmq"

	"github.com/linxGnu/goseaweedfs"
)

// This file will not be regenerated automatically.
//
// It serves as dependency injection for your app, add any dependencies you require here.

type Resolver struct {
	Config *config.Config
	DB     *mongo.Connection
	Queue  *rabbitmq.Connection
	CDN    *goseaweedfs.Seaweed
}
