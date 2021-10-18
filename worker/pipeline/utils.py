from datetime import datetime


def get_creation_time(exif_datetime):
  """This converts exif date time string into iso format"""
  return datetime.strptime(exif_datetime, '%Y:%m:%d %H:%M:%S').isoformat()
