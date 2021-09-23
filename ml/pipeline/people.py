"""People"""
from .component import Component


class People(Component):
  """People Component"""
  def __init__(self, db, oid, image_url):
    super().__init__('people', db, oid, image_url)

  def process(self):
    print(f'[people]: {self.oid} {self.image_url}')
