"""Worker"""
import os
import pika
from pymongo import MongoClient
from callback import Callback


client = MongoClient(os.getenv('DB_URI'))
db = client[os.getenv('DB_NAME')]

def start_consumers():
  """Init rabbitmq connection and start consumers"""
  connection = pika.BlockingConnection(pika.URLParameters(os.getenv('QUEUE_URI')))
  channel = connection.channel()
  callback = Callback(db=db)
  message_callback = callback.process
  channel.basic_consume(queue=os.getenv('QUEUE_NAME'), auto_ack=False,
                        on_message_callback=message_callback)
  channel.start_consuming()

if __name__ == "__main__":
  print('starting worker')
  start_consumers()
