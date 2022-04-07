"""Component"""
import os
from bson.objectid import ObjectId


class Component:
  """Component"""
  def __init__(self, name, db, oid, image_url, mime_type):
    self.name = name
    self.db = db
    self.oid = oid
    self.image_url = image_url
    self.mime_type = mime_type

  def clear_files(self):
    """Clears downloaded or any processing files"""
    if os.path.exists(self.file_name):
      os.remove(self.file_name)

  @property
  def file_name(self):
    """Returns the downloaded file name"""
    return f'image-{self.oid}'

  def update(self, data):
    """Updates database with the pipeline result"""
    self.db['mediaitems'].update_one({'_id': ObjectId(self.oid)}, data)

  def process(self):
    """Component Process"""
    raise NotImplementedError
