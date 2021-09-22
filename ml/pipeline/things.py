"""Things"""
from .component import Component


class Things(Component):
  """Things Component"""
  def __init__(self):
    super().__init__('things', 'pipeline.things')

  def process(self, oid, image_url):
    print(oid)
    print(image_url)
