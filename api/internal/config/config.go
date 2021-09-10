package config

import "github.com/kelseyhightower/envconfig"

type (
	Database struct {
		URI  string `envconfig:"DB_URI" default:"mongodb://root:root@database:5010/iris?authSource=admin"`
		Name string `enconfig:"DB_NAME" default:"iris"`
	}

	Config struct {
		Database
		Port int `envconfig:"PORT" default:"5001"`
	}
)

func Init() (config Config, err error) {
	err = envconfig.Process("", &config)

	return
}
