"""Things"""
import requests
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from .component import Component


class Things(Component):
  """Things Component"""
  def __init__(self, db, oid, image_url, mime_type):
    super().__init__('things', db, oid, image_url, mime_type)
    self.INFERENCE_TYPES = [
      'object_detection', 'image_classification'
    ]
    self.MODELS = [
      'maskrcnn', 'resnet152'
    ]

  def get_inference_results(self, inference_type):
    """Calls torchserve inference api and returns response"""
    model_name = self.MODELS[0] if inference_type == self.INFERENCE_TYPES[0] else self.MODELS[1]
    data = None
    with open(self.file_name, 'rb') as f:
      data = f.read()
    headers = {'Content-Type': self.mime_type}
    res = requests.post(f'http://ml:5002/predictions/{model_name}', data=data, headers=headers)
    if res.status_code == 200:
      data = res.json()
      print(f'{inference_type} {data}')
      return data
    print(f'error while making inference request, status code: {res.status_code}')
    return {}

  def upsert_entity(self, data):
    """Upserts things entity"""
    entity_oids = []
    for cat_class in data:
      cat_class = cat_class.replace('_', ' ')
      result = self.db['entities'].find_one_and_update(
        {'name': cat_class, 'entityType': 'things'},
        {'$set': { 'name': cat_class, 'imageUrl': self.image_url }},
        upsert=True,
        return_document=ReturnDocument.AFTER
      )
      self.db['entities'].update_one(
        {'_id': result['_id']},
        {'$addToSet': {'mediaItems': ObjectId(self.oid)}},
      )
      entity_oids.append(result['_id'])
    print(f'[things]: {entity_oids}')
    return entity_oids

  def process(self):
    # make inference call for object detection
    od_result = self.get_inference_results(self.INFERENCE_TYPES[0])
    ic_result = self.get_inference_results(self.INFERENCE_TYPES[1])
    if 'content_categories' not in od_result:
      od_result['content_categories'] = []
    if 'content_categories' not in ic_result:
      ic_result['content_categories'] = []
    if 'classes' not in od_result:
      od_result['classes'] = []
    if 'classes' not in ic_result:
      ic_result['classes'] = []
    content_categories = list(set(od_result['content_categories'] + ic_result['content_categories']))
    classes = list(set(od_result['classes'] + ic_result['classes']))

    entity_oids = self.upsert_entity(classes)
    self.update({ '$set': { 'contentCategories': content_categories }, '$addToSet': { 'entities': { '$each': entity_oids } } })
