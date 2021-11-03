"""People"""
import os
import requests
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from .utils import get_closest_people, upload_image
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
    res = requests.post(f'{os.getenv("ML_URL")}/predictions/facenet', data=data, headers=headers)
    if res.status_code == 200:
      data = res.json()
      return data
    print(f'error while making inference request, status code: {res.status_code}')
    return result_classes

  def upsert_entity(self, data):
    """Upserts people entity"""
    if 'name' in data:
      result = self.db['entities'].find_one_and_update(
        {'name': data['name'], 'entityType': 'people'},
        {'$set': data},
        upsert=True,
        return_document=ReturnDocument.AFTER
      )
      self.db['entities'].update_one(
        {'_id': result['_id']},
        {'$addToSet': {'embeddings': data['embedding'], 'mediaItems': ObjectId(self.oid)}},
      )
      print(f'[people]: {result["_id"]}')
      return result['_id']

    self.db['entities'].update_one(
      {'_id': data['_id']},
      {'$addToSet': {'embeddings': data['embedding'], 'mediaItems': ObjectId(self.oid)}},
    )
    print(f'[people]: {data["_id"]}')
    return data['_id']

  def cluster_people(self, result):
    """Cluster people from detected faces and embeddings"""
    entity_oids = []
    for val in result:
      people = list(self.db['entities'].find({'entityType': 'people'}))
      insert_people = None
      if len(people) == 0:
        image_url = upload_image(val['data'])
        insert_people = {'name': 'Face #1', 'imageUrl': image_url, 'embedding': val['embedding']}
      else:
        _id = get_closest_people(people, val['embedding'])
        insert_people = {'_id': _id, 'embedding': val['embedding']}
        if _id is None:
          image_url = upload_image(val['data'])
          insert_people = {'name': f'Face #{len(people)+1}', 'imageUrl': image_url, 'embedding': val['embedding']}
      entity_oids.append(self.upsert_entity(insert_people))
    return entity_oids

  def process(self):
    try:
      result = self.get_inference_results()
      entity_oids = self.cluster_people(result)
      self.update({ '$addToSet': { 'entities': { '$each': entity_oids } } })
    except Exception as e:
      print(f'some exception while processing people: {str(e)}')
    finally:
      self.clear_files()
