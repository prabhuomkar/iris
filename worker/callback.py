import os
import json
import urllib.request


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

    # download the file for usage
    oid, image_url, mime_type = data['id'], data['imageUrl'], data['mimeType']
    urllib.request.urlretrieve(image_url, f'image-{oid}')
    print(f'[{self.queue}]: downloaded file: image-{oid} from url: {image_url} mime: {mime_type}')

    # start the component
    component = self.component(self.db, oid, image_url, mime_type)
    component.process()

    # manually acknowledge the message
    os.remove(f'image-{oid}')
    ch.basic_ack(delivery_tag=method.delivery_tag)
