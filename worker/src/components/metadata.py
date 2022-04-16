"""Metadata Component"""
import io
import datetime
import exiftool
import rawpy
import imageio
from PIL import Image
from pillow_heif import register_heif_opener

from utils import upload_mediaitem, get_preview_file_name, get_source_file_name


class Metadata():
  """Worker Metadata Component"""
  def __init__(self, db):
    self.db = db
    self.metadata_datetime_format = '%Y:%m:%d %H:%M:%S'
    self.std_images = [
      'image/avif', 'image/bmp', 'image/gif', 'image/heic',
      'image/heif', 'image/ico', 'image/pipeg', 'image/png',
      'image/tiff', 'image/webp', 'image/x-icon', 'image/jpeg'
    ]

  def _get_creation_time(self, metdata_datetime):
    """Returns valid datetime from metadata creation time"""
    return datetime.datetime.strptime(metdata_datetime, self.metadata_datetime_format).replace(tzinfo=datetime.timezone.utc).isoformat()

  def _extract_metadata(self, metadata):
    """Extracts metadata which is required to persist in database"""
    wh_splits = metadata['Composite:ImageSize'].split()
    media_metadata = {
      'creationTime': self._get_creation_time(str(metadata['EXIF:DateTimeOriginal'])) if 'EXIF:DateTimeOriginal' in metadata \
        else self._get_creation_time(str(metadata['EXIF:CreateDate'])) if 'EXIF:CreateDate' in metadata \
        else self._get_creation_time(str(metadata['MakerNotes:DateTimeOriginal'])) if 'MakerNotes:DateTimeOriginal' in metadata else None,
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
    return media_metadata

  def _extract_preview_bytes(self, metadata, filename):
    """Extracts preview bytes which will be uploaded to cdn"""
    # use pillow to convert images of standard types
    data = None
    if 'File:MIMEType' in metadata and \
      metadata['File:MIMEType'] in self.std_images:
      register_heif_opener()
      image = Image.open(filename)
      image_bytes = io.BytesIO()
      image = image.convert('RGB')
      image.save(image_bytes, format='JPEG')
      data = image_bytes.getvalue()
    else:
      # use rawpy to convert raw images to standard jpeg
      with rawpy.imread(filename) as raw:
        rgb = raw.postprocess()
      data = imageio.imsave(imageio.RETURN_BYTES, rgb, format='jpg')
    return data

  def run(self, event):
    """Run metadata component"""
    try:
      # later(omkar): update 'status': 'PROCESSING'
      with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(get_source_file_name(event))
        metadata = metadata[0] if len(metadata) > 0 else {}
        if len(metadata.keys()) > 0:
          # extract raw image and upload to cdn
          mediaitem_preview_bytes = self._extract_preview_bytes(metadata, get_source_file_name(event))
          if mediaitem_preview_bytes is not None:
            Image.open(io.BytesIO(mediaitem_preview_bytes)).save(get_preview_file_name(event))
            preview_url = upload_mediaitem(get_preview_file_name(event))
            # later(omkar): update 'status': 'READY', 'previewUrl': preview_url
          else:
            # later(omkar): update 'status': 'FAILED'
            print(f'cannot get preview bytes for mediaitem {id}')
          # extract metdata
          mediaitem_metadata = self._extract_metadata(metadata)
          print('[metadata]', mediaitem_metadata, preview_url)
        else:
          print('no metadata available via exiftool')
          # later(omkar): mark as upload failed and delete from CDN
    except Exception as e:
      print(f'error executing metadata component: {str(e)}')
    finally:
      print(f'finished executing metdata component for mediaitem: {event["id"]}')
