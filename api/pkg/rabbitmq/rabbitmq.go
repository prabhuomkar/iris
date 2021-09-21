package rabbitmq

import (
	"github.com/streadway/amqp"
)

// Connection maintains instance of client connection
type Connection struct {
	Connection *amqp.Connection
	Channel    *amqp.Channel
	Exchange   string
}

// Init will initialize rabbitmq connection
func Init(amqpURI, exchange string) (*Connection, error) {
	connection, err := amqp.Dial(amqpURI)
	if err != nil {
		return nil, err
	}

	channel, err := connection.Channel()
	if err != nil {
		return nil, err
	}

	return &Connection{
		Connection: connection,
		Channel:    channel,
		Exchange:   exchange,
	}, nil
}

// Disconnect will close the existing rabbitmq connection instance
func (c *Connection) Disconnect() error {
	// later(omkar): handle disconnects
	return nil
}

// Publish will send a message to queue
func (c *Connection) Publish(routingKey string, message []byte) error {
	return c.Channel.Publish(
		c.Exchange, routingKey, false, false,
		amqp.Publishing{
			ContentType: "application/json",
			Body:        message,
		},
	)
}
