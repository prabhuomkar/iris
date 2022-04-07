import json
import os
from threading import Thread
import urllib.request
from pipeline import Metadata, People, Places, Things


class Callback:
  """RabbitMQ Callback"""
  def __init__(self, db):
    self.db = db
    self.components = [Metadata, Places]

  def process(self, ch, method, ___, body):
    """Callback processing"""
    print(f'consumed event from queue: {str(body)}')

    data = json.loads(body)
    # extract details from message
    oid, mediaitem_url, mime_type = data['id'], data['imageUrl'], data['mimeType']
    file_id = f'mediaitem-{oid}'
    try:
      # download the mediaitem
      urllib.request.urlretrieve(mediaitem_url, file_id)
      # start the pipeline processing
      threads = [Thread(target=component(self.db, oid, mediaitem_url, mime_type).process, args=()) for component in self.components]
      [thread.start() for thread in threads]
      [thread.join() for thread in threads]
    except Exception as e:
      print(f'some exception while downloading and running pipeline component for mediaitem: {str(e)}')
    finally:
      if os.path.exists(file_id):
        print(f'clearing the downloaded mediaitem: {file_id}')
        os.remove(file_id)
      # manually acknowledge the message
      ch.basic_ack(delivery_tag=method.delivery_tag)
