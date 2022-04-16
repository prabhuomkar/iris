"""RabbitMQ Consumer"""
import time
from threading import Thread
import pika


class RabbitMQConsumer():
  """RabbitMQ Consumer"""
  def __init__(self, uri, queue, execute):
    """Initialize RabbitMQ Consumer"""
    self._queue = queue
    self._callable = execute
    self._url = uri
    self.should_reconnect = False
    self.was_consuming = False
    self._connection = None
    self._channel = None
    self._closing = False
    self._consumer_tag = None
    self._consuming = False
    self._prefetch_count = 4

  def connect(self):
    """Open rabbitmq connection"""
    return pika.SelectConnection(
      parameters=pika.URLParameters(self._url),
      on_open_callback=self.on_connection_open,
      on_open_error_callback=self.on_connection_open_error,
      on_close_callback=self.on_connection_close)

  def close(self):
    """Close rabbitmq connection"""
    self._consuming = False
    if self._connection.is_closing or self._connection.is_closed:
      print('rabbitmq connection is closing or already closed')
    else:
      self._connection.close()

  def on_connection_open(self, _):
    """When rabbitmq connection is opened"""
    self.open_channel()

  def on_connection_open_error(self, _, err):
    """When rabbitmq connection throws error on opening"""
    print(f'error while opening rabbit connection {str(err)}')
    self.reconnect()

  def on_connection_close(self, _, reason):
    """When rabbitmq connection is closed"""
    self._channel = None
    if self._closing:
      self._connection.ioloop.stop()
    else:
      print(f'rabbit connection closed, reconnect necessary: {reason}')
      self.reconnect()

  def reconnect(self):
    """Reopening rabbitmq connection"""
    self.should_reconnect = True
    self.stop()

  def open_channel(self):
    """Open rabbitmq connection channel"""
    self._connection.channel(on_open_callback=self.on_channel_open)

  def close_channel(self):
    """Close rabbitmq connection channel"""
    self._channel.close()

  def on_consumer_cancelled(self, _):
    """On rabbitmq consumer is cancelled"""
    if self._channel:
      self._channel.close()

  def on_channel_open(self, channel):
    """On rabbitmq connection channel opened callback"""
    self._channel = channel
    self._channel.add_on_close_callback(self.on_channel_close)
    self._channel.basic_qos(prefetch_count=self._prefetch_count)
    self.start_consuming()

  def on_channel_close(self, _, reason):
    """On rabbitmq connection channel closed callback"""
    print(f'closed rabbitmq connection channel, reason: {reason}')
    self.close()

  def start_consuming(self):
    """Rabbitmq starts consuming messages"""
    self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
    self._consumer_tag = self._channel.basic_consume(queue=self._queue,
      on_message_callback=self.on_message)
    self.was_consuming = True
    self._consuming = True

  def stop_consuming(self):
    """Rabbitmq stops consuming messages"""
    if self._channel:
      self._channel.basic_cancel(self._consumer_tag)
      self.close_channel()

  def on_message(self, _, basic_deliver, __, body):
    """Acknowledge the message on receiving"""
    if self._callable:
      Thread(target=self._callable, args=(body,)).start()
      self._channel.basic_ack(basic_deliver.delivery_tag)

  def start(self):
    """Start rabbitmq consumer"""
    self._connection = self.connect()
    self._connection.ioloop.start()

  def stop(self):
    """Stop rabbitmq consumer"""
    if not self._closing:
      self._closing = True
      if self._consuming:
        self.stop_consuming()
        self._connection.ioloop.start()
      else:
        self._connection.ioloop.stop()

class Consumer():
  """Consumer with retry connection"""
  def __init__(self, uri, queue, execute):
    self._reconnect_delay = 0
    self._uri = uri
    self._queue = queue
    self._execute = execute
    self._consumer = RabbitMQConsumer(self._uri, self._queue, self._execute)

  def run(self):
    """Start consumer"""
    while True:
      try:
        self._consumer.start()
      except KeyboardInterrupt:
        self._consumer.stop()
        break
      self.maybe_reconnect()

  def maybe_reconnect(self):
    """Reconnect and create new instance of consumer"""
    if self._consumer.should_reconnect:
      self._consumer.stop()
      reconnect_delay = self.get_reconnect_delay()
      print(f'reconnecting to rabbitmq after {reconnect_delay} seconds')
      time.sleep(reconnect_delay)
      self._consumer = RabbitMQConsumer(self._uri, self._queue, self._execute)

  def get_reconnect_delay(self):
    """Get retry connectional time interval"""
    self._reconnect_delay = 0 if self._consumer.was_consuming else self._reconnect_delay*2
    return min(30, self._reconnect_delay)
