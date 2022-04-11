"""Preview"""
import io
import exiftool
import rawpy
import imageio
from PIL import Image
from pillow_heif import register_heif_opener
from .component import Component
from .utils import upload_image


register_heif_opener()

class Preview(Component):
  """Preview Component"""
  def __init__(self, db, oid, filename, mediaitem_url):
    super().__init__('preview', db, oid, filename, mediaitem_url)
    self.std_images = ['image/jpeg', 'image/png', 'image/tiff', 'image/webp',
      'image/bmp', 'image/ico', 'image/heic', 'image/heif', 'image/gif']

  def process(self):
    try:
      self.update({'$set': {'status': 'PROCESSING'}})
      with exiftool.ExifTool() as et:
        metadata = et.get_metadata(self.file_name)
        data = None
        if len(metadata.keys()) > 0 and 'File:MIMEType' in metadata and \
          metadata['File:MIMEType'] in self.std_images:
          image = Image.open(self.file_name)
          image_bytes = io.BytesIO()
          image = image.convert('RGB')
          image.save(image_bytes, format='JPEG')
          data = image_bytes.getvalue()
        else:
          with rawpy.imread(self.file_name) as raw:
            rgb = raw.postprocess()
          data = imageio.imsave(imageio.RETURN_BYTES, rgb, format='jpg')
        if data is not None:
          preview_url = upload_image(data.decode('latin1'))
          self.update({'$set': {
            'status': 'READY',
            'previewUrl': preview_url,
          }})
        else:
          self.update({'$set': {
            'status': 'FAILED',
          }})
          print(f'cannot get preview bytes for mediaitem {self.oid}')
    except Exception as e:
      print(f'some exception while processing preview for mediaitem {self.oid}: {str(e)}')
