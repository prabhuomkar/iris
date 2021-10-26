from datetime import datetime


def get_creation_time(exif_datetime):
  """This converts exif date time string into iso format"""
  return datetime.strptime(exif_datetime, '%Y:%m:%d %H:%M:%S').isoformat()

def get_image_classification_classes(data, topK = 3):
  """Gets topK classes from results of image classification"""
  result_classes = []
  data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
  for i, key in enumerate(data):
    if data[key] > 0.80:
      result_classes.append(key)
      if data[key] > 0.90:
        break
    if i == topK - 1:
      break
  return result_classes

def get_object_detection_classes(data, topK = 3):
  """Gets topK classes from results of object detection"""
  result_classes = []
  max_prob_found = False
  data = list(sorted(data, key=lambda x: x['score'], reverse=True))
  for i, elem in enumerate(data):
    keys = list(elem.keys())
    if 'score' in keys and elem['score'] > 0.80:
      result_classes.append(keys[0])
      if elem['score'] > 0.90:
        max_prob_found = True
    elif max_prob_found:
      break
    if i == topK - 1:
      break
  return result_classes
