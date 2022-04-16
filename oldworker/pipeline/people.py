"""People"""
import os
from PIL import Image
import torch
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from facenet_pytorch import MTCNN, InceptionResnetV1
from .utils import get_closest_people, upload_image
from .component import Component


class People(Component):
  """People Component"""
  def __init__(self, db, oid, filename, mediaitem_url):
    super().__init__('people', db, oid, filename, mediaitem_url)
    self.mtcnn_model = MTCNN(margin=48, image_size=240, keep_all=True)
    self.resnet_model = InceptionResnetV1(pretrained='vggface2').eval()

  def get_inference_results(self):
    """Calls torchserve inference api and returns response"""
    # run pytorch inference
    res_bytes = []
    ten_imgs = []
    data = Image.open(f'{self.file_name}')
    imgs, probs = self.mtcnn_model(data, save_path=f'{self.file_name}-people-result.jpg', return_prob=True)
    result = []
    if imgs is not None:
      for i in range(1, len(imgs)+1):
        if probs[i-1] >= 0.99:
          ten_imgs.append(imgs[i-1])
          img_path = f'{self.file_name}-people-result.jpg' if i == 1 else f'{self.file_name}-people-result_{i}.jpg'
          with open(img_path, 'rb') as f:
            res_bytes.append(f.read())
            os.remove(img_path)
      if len(ten_imgs) > 0:
        stacked_imgs = torch.stack(ten_imgs) # pylint: disable=no-member
        embeddings = self.resnet_model(stacked_imgs)
        result = [
          { 'data': res.decode('latin1'), 'embedding': embed.tolist() } for res, embed in zip(res_bytes, embeddings)
        ]
    return result

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
    entity_images = []
    for val in result:
      people = list(self.db['entities'].find({'entityType': 'people'}))
      insert_people = None
      mediaitem_url = upload_image(val['data'])
      if len(people) == 0:
        insert_people = {'name': 'Face #1', 'embedding': val['embedding'], 'previewMediaItem': ObjectId(self.oid)}
      else:
        _id = get_closest_people(people, val['embedding'])
        insert_people = {'_id': _id, 'embedding': val['embedding']}
        if _id is None:
          insert_people = {'name': f'Face #{len(people)+1}', 'embedding': val['embedding']}
      entity_id = self.upsert_entity(insert_people)
      entity_oids.append(entity_id)
      entity_images.append({'entityId': entity_id, 'previewUrl': mediaitem_url})
    return entity_oids, entity_images

  def process(self):
    try:
      result = self.get_inference_results()
      entity_oids, entity_images = self.cluster_people(result)
      self.update({ '$addToSet': {
        'entities': { '$each': entity_oids },
        'faces': { '$each': entity_images },
      }})
    except Exception as e:
      print(f'some exception while processing people for mediaitem {self.oid}: {str(e)}')
