import os
from pymongo import MongoClient

from services import Consumer
from components import Pipeline


if __name__ == '__main__':
  # initialize database connection
  client = MongoClient(os.getenv('DB_URI'))
  db = client[os.getenv('DB_NAME')]
  # initialize pipeline
  pipeline = Pipeline(db=db)
  # initialize consumer
  consumer = Consumer(uri=os.getenv('QUEUE_URI'), queue=os.getenv('INPUT_QUEUE_NAME'), execute=pipeline.process)
  consumer.run()
