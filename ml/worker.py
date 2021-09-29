"""ML Worker"""
import json
import urllib.request
import pika
from pymongo import MongoClient
from pipeline import Metadata, People, Places, Things

client = MongoClient('mongodb://root:root@database:5010/iris?authSource=admin')
db = client['iris']

queues = ['pipeline.metadata', 'pipeline.people', 'pipeline.places', 'pipeline.things']

def message_callback(ch, method, ___, body):
  """RabbitMQ Message Callback"""
  data = json.loads(body)
  print(f'[message]: {data}')

  # download the file for usage
  oid, image_url = data['id'], data['imageUrl']
  urllib.request.urlretrieve(image_url, f'image-{oid}')
  print(f'[worker]: downloaded file: image-{oid} from url: {image_url}')

  # initialize the pipeline
  pipeline = [Metadata, People, Places, Things]

  # start the pipeline
  for _component in pipeline:
    component = _component(db, oid, image_url)
    component.process()

  # manually acknowledge the message
  ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumers():
  """Init rabbitmq connection and start consumers"""
  credentials = pika.PlainCredentials('root', 'root')
  connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='queue', port='5030', credentials=credentials))
  channel = connection.channel()
  for queue in queues:
    channel.basic_consume(queue=queue,
                        auto_ack=False,
                        on_message_callback=message_callback)
  channel.start_consuming()

if __name__ == "__main__":
  start_consumers()
