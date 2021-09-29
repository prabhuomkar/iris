"""Things"""
from .component import Component


class Things(Component):
  """Things Component"""
  def __init__(self, db, oid, image_url):
    super().__init__('things', db, oid, image_url)

  def process(self):
    print(f'[things]: {self.oid} {self.image_url}')
