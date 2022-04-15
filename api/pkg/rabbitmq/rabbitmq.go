package rabbitmq

import (
	"log"

	"github.com/streadway/amqp"
)

// Connection maintains instance of client connection
type Connection struct {
	Connection *amqp.Connection
	Channel    *amqp.Channel
	Queue      string
}

// Init will initialize rabbitmq connection
func Init(amqpURI, queue string) (*Connection, error) {
	connection, err := amqp.Dial(amqpURI)
	if err != nil {
		log.Printf("error connecting to queue rabbitmq: %+v", err)

		return nil, err
	}

	channel, err := connection.Channel()
	if err != nil {
		log.Printf("error opening channel of queue rabbitmq: %+v", err)

		return nil, err
	}

	log.Printf("connected to queue rabbitmq")

	return &Connection{
		Connection: connection,
		Channel:    channel,
		Queue:      queue,
	}, nil
}

// Disconnect will close the existing rabbitmq connection instance
func (c *Connection) Disconnect() error {
	return c.Connection.Close()
}

// Publish will send a message to rabbitmq exchange
func (c *Connection) Publish(message []byte) error {
	log.Printf("publishing message to queue rabbitmq: %s", string(message))

	return c.Channel.Publish(
		"", c.Queue, false, false,
		amqp.Publishing{
			ContentType: "application/json",
			Body:        message,
		},
	)
}
