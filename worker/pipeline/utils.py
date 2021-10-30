from datetime import datetime
from collections import Counter
from annoy import AnnoyIndex
from bson.objectid import ObjectId


def get_creation_time(exif_datetime):
  """This converts exif date time string into iso format"""
  return datetime.strptime(exif_datetime, '%Y:%m:%d %H:%M:%S').isoformat()

def get_closest_people(people, embedding):
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
  similar_ids, dist = t.get_nns_by_item(0, n=11, include_distances=True)
  similar_ids = [s for s,d in zip(similar_ids, dist) if d <= 1.0][1:]
  distinct_ids = [str(peep_embeds[sid]) for sid in similar_ids]
  max_occ_dist_id = Counter(distinct_ids).most_common(1)
  if max_occ_dist_id is not None and len(max_occ_dist_id) > 0:
    _id = max_occ_dist_id[0][0]
    return ObjectId(_id)
  return _id
