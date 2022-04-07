"""Component"""
import os
from bson.objectid import ObjectId


class Component:
  """Component"""
  def __init__(self, name, db, oid, mediaitem_url, mime_type):
    self.name = name
    self.db = db
    self.oid = oid
    self.mediaitem_url = mediaitem_url
    self.mime_type = mime_type

  @property
  def file_name(self):
    """Returns the downloaded file name"""
    return f'mediaitem-{self.oid}'

  def update(self, data):
    """Updates database with the pipeline result"""
    self.db['mediaitems'].update_one({'_id': ObjectId(self.oid)}, data)

  def process(self):
    """Component Process"""
    raise NotImplementedError
