from datetime import datetime


def get_creation_time(exif_datetime):
  """This converts exif date time string into iso format"""
  return datetime.strptime(exif_datetime, '%Y:%m:%d %H:%M:%S').isoformat()

def get_image_classification_classes(data, topK = 3):
  """Gets topK classes from results of image classification"""
  result_classes = []
  max_score = 0
  max_score_category = ''
  for item in data:
    keys = list(item.keys())
    if 'score' in keys and item['score'] > max_score:
      max_score_category = keys[0]
    elif 'score' in keys and item['score'] > 0.8:
      result_classes.append(keys[0])
  if max_score_category not in result_classes:
    result_classes.append(max_score_category)
  return result_classes

def get_object_detection_classes(data, topK = 3):
  """Gets topK classes from results of object detection"""
  result_classes = []
  max_score = 0
  max_score_category = ''
  for item in data:
    if data[item] > max_score:
      max_score_category = item
    if data[item] > 0.8:
      result_classes.append(item)
  if max_score_category not in result_classes:
    result_classes.append(max_score_category)
  return result_classes
