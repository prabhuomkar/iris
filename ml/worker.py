"""ML Worker"""
import pika
from pymongo import MongoClient
from pipeline import Metadata, People, Places, Things

client = MongoClient('mongodb://root:root@database:5010/iris?authSource=admin')
db = client['iris']

pipeline = [Metadata(db), People(db), Places(db), Things(db)]

def start_consumers():
  """Init rabbitmq connection and start consumers"""
  credentials = pika.PlainCredentials('root', 'root')
  connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='queue', port='5030', credentials=credentials))
  channel = connection.channel()
  for component in pipeline:
    channel.basic_consume(queue=component.queue,
                        auto_ack=False,
                        on_message_callback=component.callback)
  channel.start_consuming()

if __name__ == "__main__":
  start_consumers()
