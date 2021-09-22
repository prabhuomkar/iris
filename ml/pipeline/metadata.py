"""Metadata"""
import exifread
from .component import Component


class Metadata(Component):
  """Metadata Component"""
  def __init__(self, db):
    super().__init__('metadata', 'pipeline.metadata', db)

  def process(self, oid, image_url):
    self.download(oid, image_url)
    f = open(f'image-{oid}', 'rb')
    tags = exifread.process_file(f)
    self.update(oid, {
      'mediaMetadata': {
        'creationTime': str(tags['EXIF DateTimeOriginal']) if 'EXIF DateTimeOriginal' in tags else '',
        'width': tags['EXIF ExifImageLength'].values[0] if 'EXIF ExifImageLength' in tags else '',
        'height': tags['EXIF ExifImageWidth'].values[0] if 'EXIF ExifImageWidth' in tags else '',
        'photo': {
          'cameraMake': str(tags['Image Make']) if 'Image Make' in tags else '',
          'cameraModel': str(tags['Image Model']) if 'Image Model' in tags else '',
          'focalLength': str(tags['EXIF FocalLength'].values[0].decimal()) if 'EXIF FocalLength' in tags else '',
          'apertureFNumber': str(tags['EXIF FNumber'].values[0].decimal()) if 'EXIF FNumber' in tags else '',
          'isoEquivalent': tags['EXIF ISOSpeedRatings'].values[0] if 'EXIF ISOSpeedRatings' in tags else '',
          'exposureTime': str(tags['EXIF ExposureTime']) if 'EXIF ExposureTime' in tags else '',
        },
      }
    })
