import json
import os
from threading import Thread
import urllib.request
from bson.objectid import ObjectId
from pipeline import Preview, Metadata, Places, People, Things


class Callback:
  """RabbitMQ Callback"""
  def __init__(self, db, channel, queue):
    self.db = db
    self.channel = channel
    self.queue = queue
    self.components = {
      os.getenv('COMMON_QUEUE_NAME'): [Preview, Metadata],
      os.getenv('INTERNAL_QUEUE_NAME'): []
    }

  def process(self, ch, method, ___, body):
    """Callback processing"""
    print(f'consumed event from queue: {str(body)}')

    data = json.loads(body)
    # extract details from message
    oid, filename, mediaitem = data['id'], data['fileName'], data['mediaItem']
    mediaitem_url = mediaitem['downloadUrl']
    # extract what components need to be initialized
    actions = data['actions'] if 'actions' in data else []
    if 'places' in actions and Places not in self.components and self.queue == os.getenv('COMMON_QUEUE_NAME'):
      self.components[self.queue].append(Places)
    if 'people' in actions and People not in self.components and self.queue == os.getenv('INTERNAL_QUEUE_NAME'):
      self.components[self.queue].append(People)
    if 'things' in actions and Things not in self.components and self.queue == os.getenv('INTERNAL_QUEUE_NAME'):
      self.components[self.queue].append(Things)
    file_id = f'mediaitem-{oid}-{filename}'
    try:
      # download the mediaitem
      urllib.request.urlretrieve(mediaitem_url, file_id)
      # start the pipeline processing
      threads = [Thread(target=component(self.db, oid, filename, mediaitem_url).process, args=()) \
        for component in self.components[self.queue]]
      [thread.start() for thread in threads] # pylint: disable=expression-not-assigned
      [thread.join() for thread in threads] # pylint: disable=expression-not-assigned
    except Exception as e:
      print(f'some exception while downloading and running pipeline component for queue: {self.queue} and mediaitem: {str(e)}')
    finally:
      # manually acknowledge the message
      ch.basic_ack(delivery_tag=method.delivery_tag)
      if os.path.exists(file_id):
        print(f'clearing the downloaded mediaitem: {file_id}')
        os.remove(file_id)
      # send for inferencing
      if self.queue == os.getenv('COMMON_QUEUE_NAME') and len(self.components[os.getenv('INTERNAL_QUEUE_NAME')]) > 0:
        res = self.db['mediaitems'].find_one({'_id': ObjectId(data['id'])})
        if res is not None:
          data['mediaItem']['downloadUrl'] = res['previewUrl']
          self.channel.basic_publish(exchange='', routing_key=os.getenv('INTERNAL_QUEUE_NAME'), body=json.dumps(data))
