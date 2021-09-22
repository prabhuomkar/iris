"""People"""
from .component import Component


class People(Component):
  """People Component"""
  def __init__(self, db):
    super().__init__('people', 'pipeline.people', db)

  def process(self, oid, image_url):
    print(oid)
    print(image_url)
