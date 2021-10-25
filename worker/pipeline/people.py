"""People"""
from .component import Component


class People(Component):
  """People Component"""
  def __init__(self, db, oid, image_url, mime_type):
    super().__init__('people', db, oid, image_url, mime_type)

  def process(self):
    print(f'[people]: {self.oid} {self.image_url}')
