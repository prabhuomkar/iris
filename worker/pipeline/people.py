"""People"""
import requests
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from .component import Component


class People(Component):
  """People Component"""
  def __init__(self, db, oid, image_url, mime_type):
    super().__init__('people', db, oid, image_url, mime_type)

  def get_inference_results(self):
    """Calls torchserve inference api and returns response"""
    result_classes = []
    data = None
    with open(self.file_name, 'rb') as f:
      data = f.read()
    headers = {'Content-Type': self.mime_type}
    res = requests.post('http://ml:5002/predictions/facenet', data=data, headers=headers)
    if res.status_code == 200:
      data = res.json()
      return data
    print(f'error while making inference request, status code: {res.status_code}')
    return result_classes

  def upsert_entity(self, data):
    """Upserts people entity"""
    entity_oids = []
    for face in data:
      result = self.db['entities'].find_one_and_update(
        {'name': face['name'] if 'name' in face else '', 'entityType': 'people'},
        {'$set': data},
        upsert=True,
        return_document=ReturnDocument.AFTER
      )
      self.db['entities'].update_one(
        {'_id': result['_id']},
        {'$addToSet': {'embeddings': face['embedding'], 'mediaItems': ObjectId(self.oid)}},
      )
      entity_oids.append(result['_id'])
    print(f'[people]: {entity_oids}')
    return entity_oids

  def process(self):
    result = self.get_inference_results()
    print(len(result))
    # for val in result:
      # print(val['data'])
      # print(val['embedding'])
    # generate { 'name': '<get from clustering>', 'imageUrl': '<from cdn>', 'embedding': '<from val>' }
    people = []
    entity_oids = self.upsert_entity(people)
    self.update({ '$addToSet': { 'entities': { '$each': entity_oids } } })
