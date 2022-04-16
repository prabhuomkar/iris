"""CDN Utils"""
import os
import urllib
from pyseaweed import WeedFS


def upload_mediaitem(filename) -> str:
  """Uploads mediaitem to CDN"""
  w = WeedFS(os.getenv('CDN_URL'), int(os.getenv('CDN_PORT')))
  fid = w.upload_file(filename)
  return w.get_file_url(fid)

def download_mediaitem(download_url, filename) -> bool:
  """Downloads mediaitem from CDN"""
  try:
    urllib.request.urlretrieve(download_url, filename)
    return True
  except Exception as e:
    print(f'error downloading file: {str(e)}')
  return False
