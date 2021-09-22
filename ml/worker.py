"""ML Worker"""
import pika
from pipeline import Metadata, People, Places, Things


pipeline = [Metadata(), People(), Places(), Things()]

def consume(channel, queue, callback):
  channel.basic_consume(queue=queue,
                        auto_ack=True,
                        on_message_callback=callback)

def start_consumers():
  credentials = pika.PlainCredentials('root', 'root')
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue', port='5030', credentials=credentials))
  channel = connection.channel()
  for component in pipeline:
    consume(channel, component.queue, component.callback)
  channel.start_consuming()

if __name__ == "__main__":
  start_consumers()
