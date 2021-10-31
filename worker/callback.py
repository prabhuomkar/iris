import json
from threading import Thread


class Callback:
  """RabbitMQ Callback"""
  def __init__(self, queue, component, db):
    self.queue = queue
    self.component = component
    self.db = db

  def process(self, ch, method, ___, body):
    """Callback processing"""
    data = json.loads(body)
    print(f'[{self.queue}]: {data}')

    # extract details from message
    oid, image_url, mime_type = data['id'], data['imageUrl'], data['mimeType']

    # start the component
    component = self.component(self.db, oid, image_url, mime_type)
    Thread(target=component.process, args=()).start()

    # manually acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
