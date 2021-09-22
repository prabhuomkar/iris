"""Metadata"""
import exifread
from .component import Component


class Metadata(Component):
  """Metadata Component"""
  def __init__(self, db):
    super().__init__('metadata', 'pipeline.metadata', db)

  def process(self, oid, image_url):
    self.download(oid, image_url)
    with open(f'image-{oid}', 'rb') as f:
      tags = exifread.process_file(f)
      if len(tags.keys()) > 0:
        self.update(oid, {
          'mediaMetadata': {
            'creationTime': str(tags['EXIF DateTimeOriginal']) if 'EXIF DateTimeOriginal' in tags else None,
            'width': tags['EXIF ExifImageLength'].values[0] if 'EXIF ExifImageLength' in tags else None,
            'height': tags['EXIF ExifImageWidth'].values[0] if 'EXIF ExifImageWidth' in tags else None,
            'photo': {
              'cameraMake': str(tags['Image Make']) if 'Image Make' in tags else None,
              'cameraModel': str(tags['Image Model']) if 'Image Model' in tags else None,
              'focalLength': str(tags['EXIF FocalLength'].values[0].decimal()) if 'EXIF FocalLength' in tags else None,
              'apertureFNumber': str(tags['EXIF FNumber'].values[0].decimal()) if 'EXIF FNumber' in tags else None,
              'isoEquivalent': tags['EXIF ISOSpeedRatings'].values[0] if 'EXIF ISOSpeedRatings' in tags else None,
              'exposureTime': str(tags['EXIF ExposureTime']) if 'EXIF ExposureTime' in tags else None,
            },
          }
        })
