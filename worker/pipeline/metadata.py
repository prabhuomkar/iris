"""Metadata"""
import exiftool
from .component import Component
from .utils import get_creation_time


class Metadata(Component):
  """Metadata Component"""
  def __init__(self, db, oid, image_url, mime_type):
    super().__init__('metadata', db, oid, image_url, mime_type)

  def process(self):
    with exiftool.ExifTool() as et:
      metadata = et.get_metadata(self.file_name)
      if len(metadata.keys()) > 0:
        media_metadata = {
          'creationTime': get_creation_time(str(metadata['EXIF:DateTimeOriginal'])) if 'EXIF:DateTimeOriginal' in metadata \
            else get_creation_time(str(metadata['EXIF:CreateDate'])) if 'EXIF:CreateDate' in metadata else None,
          'width': metadata['EXIF:ExifImageHeight'] if 'EXIF:ExifImageHeight' in metadata else metadata['File:ImageHeight'] \
            if 'File:ImageHeight' in metadata else None,
          'height': metadata['EXIF:ExifImageWidth'] if 'EXIF:ExifImageHeight' in metadata else metadata['File:ImageWidth'] \
            if 'File:ImageWidth' in metadata else None,
          'location': {
            'latitude': metadata['EXIF:GPSLatitude'] if 'EXIF:GPSLatitude' in metadata \
              else metadata['Composite:GPSLatitude'] if 'Composite:GPSLatitude' in metadata else None,
            'longitude': metadata['EXIF:GPSLongitude'] if 'EXIF:GPSLongitude' in metadata \
              else metadata['Composite:GPSLongitude'] if 'Composite:GPSLongitude' in metadata else None,
          },
          'photo': {
            'cameraMake': metadata['EXIF:Make'] if 'EXIF:Make' in metadata else None,
            'cameraModel': metadata['EXIF:Model'] if 'EXIF:Model' in metadata else None,
            'focalLength': metadata['EXIF:FocalLength'] if 'EXIF:FocalLength' in metadata else None,
            'apertureFNumber': metadata['EXIF:FNumber'] if 'EXIF:FNumber' in metadata else None,
            'isoEquivalent': metadata['EXIF:ISO'] if 'EXIF:ISO' in metadata else None,
            'exposureTime': metadata['EXIF:ExposureTime'] if 'EXIF:ExposureTime' in metadata else None,
          },
        }
        print(f'[metadata]: {media_metadata}')
        self.update({'$set': {
          'mediaMetadata': media_metadata
        }})
