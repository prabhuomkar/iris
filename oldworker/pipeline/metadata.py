"""Metadata"""
import exiftool
from .component import Component
from .utils import get_creation_time



class Metadata(Component):
  """Metadata Component"""
  def __init__(self, db, oid, filename, mediaitem_url):
    super().__init__('metadata', db, oid, filename, mediaitem_url)

  def process(self):
    try:
      with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(self.file_name)
        metadata = metadata[0] if len(metadata) > 0 else {}
        if len(metadata.keys()) > 0:
          wh_splits = metadata['Composite:ImageSize'].split()
          media_metadata = {
            'creationTime': get_creation_time(str(metadata['EXIF:DateTimeOriginal'])) if 'EXIF:DateTimeOriginal' in metadata \
              else get_creation_time(str(metadata['EXIF:CreateDate'])) if 'EXIF:CreateDate' in metadata \
              else get_creation_time(str(metadata['MakerNotes:DateTimeOriginal'])) if 'MakerNotes:DateTimeOriginal' in metadata else None,
            'width': int(wh_splits[0]) if len(wh_splits) == 2 else None,
            'height': int(wh_splits[1]) if len(wh_splits) == 2 else None,
            'location': {
              'latitude': metadata['EXIF:GPSLatitude'] if 'EXIF:GPSLatitude' in metadata \
                else metadata['Composite:GPSLatitude'] if 'Composite:GPSLatitude' in metadata else None,
              'longitude': metadata['EXIF:GPSLongitude'] if 'EXIF:GPSLongitude' in metadata \
                else metadata['Composite:GPSLongitude'] if 'Composite:GPSLongitude' in metadata else None,
            },
            'photo': {
              'cameraMake': metadata['EXIF:Make'] if 'EXIF:Make' in metadata else \
              metadata['MakerNotes:Make'] if 'MakerNotes:Make' in metadata else None,
              'cameraModel': metadata['EXIF:Model'] if 'EXIF:Model' in metadata else \
              metadata['MakerNotes:Model'] if 'MakerNotes:Model' in metadata else None,
              'focalLength': metadata['EXIF:FocalLength'] if 'EXIF:FocalLength' in metadata else \
              metadata['MakerNotes:FocalLength'] if 'MakerNotes:FocalLength' in metadata else None,
              'apertureFNumber': metadata['EXIF:FNumber'] if 'EXIF:FNumber' in metadata else \
              metadata['MakerNotes:FNumber'] if 'MakerNotes:FNumber' in metadata else None,
              'isoEquivalent': metadata['EXIF:ISO'] if 'EXIF:ISO' in metadata else \
              metadata['Composite:ISO'] if 'Composite:ISO' in metadata else None,
              'exposureTime': metadata['EXIF:ExposureTime'] if 'EXIF:ExposureTime' in metadata else \
              float(metadata['MakerNotes:ExposureTime']) if 'MakerNotes:ExposureTime' in metadata else None,
            },
          }
          print(f'[metadata]: {media_metadata}')
          self.update({'$set': {
            'mimeType': metadata['File:MIMEType'],
            'mediaMetadata': media_metadata
          }})
        else:
          print(f'no metadata extracted for mediaitem: {self.oid}')
    except Exception as e:
      print(f'some exception while processing metadata for mediaitem {self.oid}: {str(e)}')
