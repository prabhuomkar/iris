"""Component"""
import json


class Component:
  """Component"""
  def __init__(self, name, queue):
    self.name = name
    self.queue = queue

  def callback(self, _, __, ___, body):
    """RabbitMQ Callback"""
    data = json.loads(body)
    print(f'[{self.name}]: {data}')
    self.process(data['id'], data['imageUrl'])

  def process(self, oid, image_url):
    """Component Process"""
    raise NotImplementedError
