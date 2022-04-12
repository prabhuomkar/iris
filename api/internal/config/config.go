package config

import (
	"fmt"
	"strings"

	"github.com/kelseyhightower/envconfig"
)

const (
	FeaturePeople = "people"
	FeaturePlaces = "places"
	FeatureThings = "things"
)

type (
	Database struct {
		URI  string `envconfig:"DB_URI" default:"mongodb://root:root@127.0.0.1:5010/iris?authSource=admin"`
		Name string `enconfig:"DB_NAME" default:"iris"`
	}

	CDN struct {
		URL       string `envconfig:"CDN_URL" default:"http://cdn-master:5020"`
		ChunkSize int64  `envconfig:"CDN_CHUNK_SIZE" default:"1048576"`
		Timeout   int64  `envconfig:"CDN_TIMEOUT" default:"5"`
	}

	Queue struct {
		URI  string `envconfig:"QUEUE_URI" default:"amqp://root:root@127.0.0.1:5030"`
		Name string `envconfig:"QUEUE_NAME" default:"iris.process"`
	}

	FeatureConfig struct {
		DisablePlaces bool `envconfig:"FEATURE_DISABLE_PLACES" default:"false"`
		DisablePeople bool `envconfig:"FEATURE_DISABLE_PEOPLE" default:"false"`
		DisableThings bool `envconfig:"FEATURE_DISABLE_THINGS" default:"false"`
	}

	Config struct {
		Database
		CDN
		Queue
		FeatureConfig
		Port int `envconfig:"PORT" default:"5001"`
	}
)

func Init() (config Config, err error) {
	err = envconfig.Process("", &config)

	return
}

func (c Config) GetMediaItemFeatures() string {
	result := []string{}

	if !c.FeatureConfig.DisablePlaces {
		result = append(result, fmt.Sprintf("%q", FeaturePlaces))
	}
	if !c.FeatureConfig.DisablePeople {
		result = append(result, fmt.Sprintf("%q", FeaturePeople))
	}
	if !c.FeatureConfig.DisableThings {
		result = append(result, fmt.Sprintf("%q", FeatureThings))
	}

	return strings.Join(result, ",")
}
