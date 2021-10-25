"""Places"""
import json
import urllib.request
import exiftool
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from .component import Component


class Places(Component):
  """Places Component"""
  def __init__(self, db, oid, image_url, mime_type):
    super().__init__('places', db, oid, image_url, mime_type)

  def upsert_place(self, address_filter, address):
    """Upserts place for future usage"""
    self.db['places'].find_one_and_update(address_filter, {'$set': address}, upsert=True, return_document=ReturnDocument.AFTER)

  def upsert_entity(self, data):
    """Upserts place entity"""
    result = self.db['entities'].find_one_and_update(
      {'name': data['name'], 'entityType': 'places'},
      {'$set': data},
      upsert=True,
      return_document=ReturnDocument.AFTER
    )
    self.db['entities'].update_one(
      {'_id': result['_id']},
      {'$addToSet': {'mediaItems': ObjectId(self.oid)}},
    )
    print(f'[place]: {result}')
    return result['_id']

  def process(self):
    with exiftool.ExifTool() as et:
      metadata = et.get_metadata(self.file_name)
      coords = []
      if 'EXIF:GPSLatitude' in metadata and 'EXIF:GPSLongitude' in metadata:
        coords.append(metadata['EXIF:GPSLatitude'])
        coords.append(metadata['EXIF:GPSLongitude'])
      elif 'Composite:GPSLatitude' in metadata and 'Composite:GPSLongitude' in metadata:
        coords.append(metadata['Composite:GPSLatitude'])
        coords.append(metadata['Composite:GPSLongitude'])
      address = {}
      address_filter = {}
      name = ''

      # get address from open street map API
      if len(coords) == 2:
        lat, lon = coords[0], coords[1]
        with urllib.request.urlopen(f'https://nominatim.openstreetmap.org/reverse.php?lat={lat}&lon={lon}&zoom=12&format=jsonv2') as url:
          data = json.loads(url.read().decode('utf-8'))
          address = data['address'] if 'address' in data else {}

      # check if address exists in database
      if len(address) > 0:
        address_filter = {}
        if 'city' in address:
          address_filter = {'city': address['city']}
          name = address['city']
        if 'town' in address:
          address_filter = {'town': address['town']}
          name = address['town']

      # update database with new place and new entity if necessary
      if len(address_filter) > 0 and len(name) > 0:
        self.upsert_place(address_filter, address)
        entity_oid = self.upsert_entity({'name': name, 'imageUrl': self.image_url})

        # update database with
        self.update({ '$addToSet': { 'entities': entity_oid } })
