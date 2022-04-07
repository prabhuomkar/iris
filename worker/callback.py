import json
from threading import Thread
import urllib.request
from pipeline import Metadata, People, Places, Things


class Callback:
  """RabbitMQ Callback"""
  def __init__(self, db):
    self.db = db
    self.components = [Metadata, People, Places, Things]

  def process(self, ch, method, ___, body):
    """Callback processing"""
    print(f'consumed event from queue: {str(body)}')

    data = json.loads(body)
    # extract details from message
    oid, image_url, mime_type = data['id'], data['imageUrl'], data['mimeType']
    try:
      # download the mediaitem
      urllib.request.urlretrieve(image_url, f'image-{oid}')
      # start the pipeline processing
      for component in self.components:
        component = component(self.db, oid, image_url, mime_type)
        Thread(target=component.process, args=()).start()
    except Exception as e:
      print(f'some exception while downloading mediaitem: {str(e)}')
    finally:
      # manually acknowledge the message
      ch.basic_ack(delivery_tag=method.delivery_tag)
