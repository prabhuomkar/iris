"""Metadata"""
from .component import Component


class Metadata(Component):
  """Metadata Component"""
  def __init__(self):
    super().__init__('metadata', 'pipeline.metadata')

  def process(self, oid, image_url):
    print(oid)
    print(image_url)
