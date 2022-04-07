package config

import (
	"github.com/kelseyhightower/envconfig"
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
		Name string `envconfig:"QUEUE_NAME" default:"iris"`
	}

	Config struct {
		Database
		CDN
		Queue
		Port int `envconfig:"PORT" default:"5001"`
	}
)

func Init() (config Config, err error) {
	err = envconfig.Process("", &config)

	return
}
