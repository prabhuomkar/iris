"""Worker"""
import os
import pika
from pymongo import MongoClient
from pipeline import Metadata, People, Places, Things
from callback import Callback

client = MongoClient(os.getenv('DB_URI'))
db = client[os.getenv('DB_NAME')]

queues = ['pipeline.metadata', 'pipeline.people', 'pipeline.places', 'pipeline.things']
components = [Metadata, People, Places, Things]

def start_consumers():
  """Init rabbitmq connection and start consumers"""
  connection = pika.BlockingConnection(pika.URLParameters(os.getenv('QUEUE_URI')))
  channel = connection.channel()
  for queue, component in zip(queues, components):
    callback = Callback(queue=queue, component=component, db=db)
    message_callback = callback.process
    channel.basic_consume(queue=queue, auto_ack=False,
                        on_message_callback=message_callback)
  channel.start_consuming()

if __name__ == "__main__":
  start_consumers()
