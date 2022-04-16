import os
from services import Consumer
from components import Pipeline


if __name__ == '__main__':
  # initialize pipeline
  pipeline = Pipeline(db=None)
  # initialize services
  consumer = Consumer(uri=os.getenv('QUEUE_URI'), queue=os.getenv('INPUT_QUEUE_NAME'), execute=pipeline.process)
  consumer.run()
