package mongo

import (
	"context"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

const (
	connectionCtxTimeout = 15
	pingCtxTimeout       = 5
)

// Connection maintains instance of client connection and database name
type Connection struct {
	Client   *mongo.Client
	Database string
}

// Init will initialize mongodb connection
func Init(mongoURI, databaseName string) (*Connection, error) {
	ctx, cancel := context.WithTimeout(context.Background(), connectionCtxTimeout*time.Second)
	defer cancel()

	client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
	if err != nil {
		log.Printf("error while connecting to mongo: %v", err)

		return nil, err
	}

	ctx, cancel = context.WithTimeout(context.Background(), pingCtxTimeout*time.Second)
	defer cancel()

	err = client.Ping(ctx, readpref.Primary())
	if err != nil {
		log.Printf("error while pinging mongo: %v", err)

		return nil, err
	}

	return &Connection{
		Client:   client,
		Database: databaseName,
	}, err
}

// Disconnect will close the existing mongodb client instance
func (c *Connection) Disconnect() error {
	ctx, cancel := context.WithTimeout(context.Background(), connectionCtxTimeout*time.Second)
	defer cancel()

	return c.Client.Disconnect(ctx)
}

// Collection will return mongo collection instance
func (c *Connection) Collection(name string) *mongo.Collection {
	return c.Client.Database(c.Database).Collection(name)
}
