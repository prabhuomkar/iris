"""Things"""
from .component import Component


class Things(Component):
  """Things Component"""
  def __init__(self, db):
    super().__init__('things', 'pipeline.things', db)

  def process(self, oid, image_url):
    print(oid)
    print(image_url)
