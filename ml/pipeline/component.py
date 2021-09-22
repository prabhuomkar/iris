"""Component"""
import json
from bson.objectid import ObjectId
import urllib.request 



class Component:
  """Component"""
  def __init__(self, name, queue, db):
    self.name = name
    self.queue = queue
    self.db = db

  def callback(self, _, __, ___, body):
    """RabbitMQ Callback"""
    data = json.loads(body)
    print(f'[{self.name}]: {data}')
    self.process(data['id'], data['imageUrl'])

  def download(self, oid, image_url):
    urllib.request.urlretrieve(image_url, f'image-{oid}')
    print(f'downloaded file image-{oid}')

  def update(self, oid, data):
    self.db['mediaitems'].update_one({'_id': ObjectId(oid)}, {'$set': data})

  def process(self, oid, image_url):
    """Component Process"""
    raise NotImplementedError
