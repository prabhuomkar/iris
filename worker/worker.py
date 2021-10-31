"""Worker"""
import pika
from pymongo import MongoClient
from pipeline import Metadata, People, Places, Things
from callback import Callback

client = MongoClient('mongodb://root:root@database:5010/iris?authSource=admin')
db = client['iris']

queues = ['pipeline.metadata', 'pipeline.people', 'pipeline.places', 'pipeline.things']
components = [Metadata, People, Places, Things]

def start_consumers():
  """Init rabbitmq connection and start consumers"""
  credentials = pika.PlainCredentials('root', 'root')
  connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='queue', port='5030', credentials=credentials))
  channel = connection.channel()
  for queue, component in zip(queues, components):
    callback = Callback(queue=queue, component=component, db=db)
    message_callback = callback.process
    channel.basic_consume(queue=queue, auto_ack=False,
                        on_message_callback=message_callback)
  channel.start_consuming()

if __name__ == "__main__":
  start_consumers()
