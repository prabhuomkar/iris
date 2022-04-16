"""Places Component"""
import json
import urllib.request
import exiftool
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from utils import get_source_file_name


class Places():
  """Worker Places Component"""
  def __init__(self, db):
    self.db = db

  def run(self, event):
    """Run places component"""
    try:
      with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(get_source_file_name(event))
        metadata = metadata[0] if len(metadata) > 0 else {}
        if len(metadata.keys()) > 0:
          coords = []
          if 'EXIF:GPSLatitude' in metadata and 'EXIF:GPSLongitude' in metadata:
            coords.append(metadata['EXIF:GPSLatitude'])
            coords.append(metadata['EXIF:GPSLongitude'])
          elif 'Composite:GPSLatitude' in metadata and 'Composite:GPSLongitude' in metadata:
            coords.append(metadata['Composite:GPSLatitude'])
            coords.append(metadata['Composite:GPSLongitude'])
          address = {}
          name = ''

          # get address from open street map API
          if len(coords) == 2:
            lat, lon = coords[0], coords[1]
            with urllib.request.urlopen(f'https://nominatim.openstreetmap.org/reverse.php?lat={lat}&lon={lon}&zoom=12&format=jsonv2') as url:
              data = json.loads(url.read().decode('utf-8'))
              address = data['address'] if 'address' in data else {}

          # check if address exists in database
          if len(address) > 0:
            if 'city' in address:
              name = address['city']
            if 'town' in address:
              name = address['town']

          if len(name) > 0:
            print('[places]', name)
            result = self.db['entities'].find_one_and_update(
              {'name': name, 'entityType': 'places'},
              {
                '$addToSet': {'mediaItems': ObjectId(event['id'])},
                '$set': {'name': name, 'entityType': 'places', 'previewMediaItem': ObjectId(event['id'])}
              },
              upsert=True,
              return_document=ReturnDocument.AFTER
            )
            self.db['mediaitems'].find_one_and_update(
              {'_id': ObjectId(event['id'])},
              {'$addToSet': {'entities': ObjectId(result['_id'])}},
            )
        else:
          print('no metadata available via exiftool')
    except Exception as e:
      print(f'error executing places component: {str(e)}')
    finally:
      print(f'finished executing places component for mediaitem: {event["id"]}')
