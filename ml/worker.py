"""ML Worker"""
import pika
from pipeline import Metadata, People, Places, Things


pipeline = [Metadata(), People(), Places(), Things()]

def start_consumers():
  credentials = pika.PlainCredentials('root', 'root')
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue', port='5030', credentials=credentials))
  channel = connection.channel()
  for component in pipeline:
    channel.basic_consume(queue=component.queue,
                        auto_ack=False,
                        on_message_callback=component.callback)
  channel.start_consuming()

if __name__ == "__main__":
  start_consumers()
