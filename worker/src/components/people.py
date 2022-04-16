"""People Component"""
import io
import os
from uuid import uuid4
from collections import Counter
import torch
from PIL import Image
from annoy import AnnoyIndex
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from facenet_pytorch import MTCNN, InceptionResnetV1

from utils import get_preview_file_name, upload_mediaitem


class People():
  """Worker People Component"""
  def __init__(self, db):
    self.db = db
    self.CLUSTER_DISTANCE = 8
    self.mtcnn_model = MTCNN(margin=48, image_size=240, keep_all=True).eval()
    self.resnet_model = InceptionResnetV1(pretrained='vggface2').eval()

  def _upsert_people(self, event, data):
    """Upserts the people in database"""
    if 'name' in data:
      result = self.db['entities'].find_one_and_update(
        {'name': data['name'], 'entityType': 'people'},
        {'$set': data},
        upsert=True,
        return_document=ReturnDocument.AFTER
      )
      self.db['entities'].update_one(
        {'_id': result['_id']},
        {'$addToSet': {'embeddings': data['embedding'], 'mediaItems': ObjectId(event['id'])}},
      )
      return result['_id']
    self.db['entities'].update_one(
      {'_id': data['_id']},
      {'$addToSet': {'embeddings': data['embedding'], 'mediaItems': ObjectId(event['id'])}},
    )
    return data['_id']

  def _get_inference_result(self, filename):
    """Run pytorch model inference and return top results"""
    res_bytes = []
    image_tensors = []
    data = Image.open(f'{filename}')
    imgs, probs = self.mtcnn_model(data, save_path=f'{filename}-people-result.jpg', return_prob=True)
    result = []
    if imgs is not None:
      for i in range(1, len(imgs)+1):
        img_path = f'{filename}-people-result.jpg' if i == 1 else f'{filename}-people-result_{i}.jpg'
        if probs[i-1] >= 0.99:
          image_tensors.append(imgs[i-1])
          tmp_img = Image.open(img_path)
          tmp_img_bytes = io.BytesIO()
          tmp_img.save(tmp_img_bytes, format='JPEG')
          res_bytes.append(tmp_img_bytes.getvalue())
        os.remove(img_path)
      if len(image_tensors) > 0:
        stacked_imgs = torch.stack(image_tensors) # pylint: disable=no-member
        embeddings = self.resnet_model(stacked_imgs)
        result = [
          { 'data': res, 'embedding': embed.tolist() } for res, embed in zip(res_bytes, embeddings)
        ]
    return result

  def _get_closest_people(self, people, embedding): # pylint: disable=too-many-locals
    """Get closest cluster name based on embedding"""
    _id = None
    # generate annoy tree
    t = AnnoyIndex(len(embedding), metric='euclidean')
    peep_embeds = [None]
    embeddings = [embedding]
    for peep in people:
      for embed in peep['embeddings']:
        embeddings.append(embed)
        peep_embeds.append(peep['_id'])
    for i, vector in enumerate(embeddings):
      t.add_item(i, vector)
    _ = t.build(len(people))
    # get similar images
    similar_ids, dist = t.get_nns_by_item(0, n=self.CLUSTER_DISTANCE, include_distances=True)
    similar_ids = [s for s,d in zip(similar_ids, dist) if d <= 1.0][1:]
    distinct_ids = [str(peep_embeds[sid]) for sid in similar_ids]
    max_occ_dist_id = Counter(distinct_ids).most_common(1)
    if max_occ_dist_id is not None and len(max_occ_dist_id) > 0:
      _id = max_occ_dist_id[0][0]
      return ObjectId(_id)
    return _id

  def _cluster_people(self, event, result):
    """Clusters people based on inference result"""
    entity_oids = []
    entity_images = []
    for val in result:
      people = list(self.db['entities'].find({'entityType': 'people'}))
      insert_people = None
      # download the face to cdn
      filename = f'{uuid4()}.jpg'
      Image.open(io.BytesIO(val['data'])).save(filename)
      mediaitem_url = upload_mediaitem(filename)
      os.remove(filename)
      # finding the the right people
      if len(people) == 0:
        insert_people = {'name': 'Face #1', 'embedding': val['embedding'], 'previewMediaItem': ObjectId(event['id'])}
      else:
        _id = self._get_closest_people(people, val['embedding'])
        insert_people = {'_id': _id, 'embedding': val['embedding']}
        if _id is None:
          insert_people = {'name': f'Face #{len(people)+1}', 'embedding': val['embedding']}
      entity_id = self._upsert_people(event, insert_people)
      entity_oids.append(entity_id)
      entity_images.append({'entityId': entity_id, 'previewUrl': mediaitem_url})
    return entity_oids, entity_images

  def run(self, event):
    """Run people component"""
    try:
      inference_result = self._get_inference_result(get_preview_file_name(event))
      entity_oids, entity_images = self._cluster_people(event, inference_result)
      self.db['mediaitems'].update_one(
        {'_id': ObjectId(event['id'])},
        {'$addToSet': {
          'entities': { '$each': entity_oids },
          'faces': { '$each': entity_images },
        }}
      )
    except Exception as e:
      print(f'error executing people component: {str(e)}')
    finally:
      print(f'finished executing people component for mediaitem: {event["id"]}')
