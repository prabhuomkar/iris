"""Component"""
from bson.objectid import ObjectId


class Component:
  """Component"""
  def __init__(self, name, db, oid, filename, mediaitem_url):
    self.name = name
    self.db = db
    self.oid = oid
    self.filename = filename
    self.mediaitem_url = mediaitem_url

  @property
  def file_name(self):
    """Returns the downloaded file name"""
    return f'mediaitem-{self.oid}-{self.filename}'

  def update(self, data):
    """Updates database with the pipeline result"""
    self.db['mediaitems'].update_one({'_id': ObjectId(self.oid)}, data)

  def process(self):
    """Component Process"""
    raise NotImplementedError
