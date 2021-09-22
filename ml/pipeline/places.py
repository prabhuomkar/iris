"""Places"""
from .component import Component


class Places(Component):
  """Places Component"""
  def __init__(self, db):
    super().__init__('places', 'pipeline.places', db)

  def process(self, oid, image_url):
    print(oid)
    print(image_url)
