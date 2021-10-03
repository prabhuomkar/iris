"""Things"""
import json
import urllib.request
from .component import Component


class Things(Component):
  """Things Component"""
  def __init__(self, db, oid, image_url):
    super().__init__('things', db, oid, image_url)
    self.INFERENCE_TYPES = [
      'object_detection', 'image_classification'
    ]
    self.MODELS = [
      'maskrcnn', 'resnet152'
    ]
    self.CONTENT_CATEGORIES = [
      'ANIMALS', 'FOOD', 'GARDENS', 'SPORT', 'PEOPLE', 'TRAVEL', 'WEDDINGS',
      'LANDSCAPES', 'SCREENSHOTS', 'WHITEBOARDS', 'BIRTHDAYS', 'NIGHT', 'FLOWERS',
      'SELFIES', 'CITYSCAPES', 'ARTS', 'CRAFTS', 'HOLIDAYS', 'FASHION', 'LANDMARKS',
      'PERFORMANCES', 'RECEIPTS', 'DOCUMENTS', 'HOUSES', 'PETS', 'UTILITY',
    ]
    self.OBJECT_DETECTION_CLASSES_TO_CATEGORY = {
      'bird': self.CONTENT_CATEGORIES[0], 'cat': self.CONTENT_CATEGORIES[0],
      'dog': self.CONTENT_CATEGORIES[0], 'horse': self.CONTENT_CATEGORIES[0],
      'sheep': self.CONTENT_CATEGORIES[0], 'cow': self.CONTENT_CATEGORIES[0],
      'elephant': self.CONTENT_CATEGORIES[0], 'bear': self.CONTENT_CATEGORIES[0],
      'zebra': self.CONTENT_CATEGORIES[0], 'giraffe': self.CONTENT_CATEGORIES[0],
      'banana': self.CONTENT_CATEGORIES[1], 'apple': self.CONTENT_CATEGORIES[1],
      'sandwich': self.CONTENT_CATEGORIES[1], 'orange': self.CONTENT_CATEGORIES[1],
      'broccoli': self.CONTENT_CATEGORIES[1], 'carrot': self.CONTENT_CATEGORIES[1],
      'hot dog': self.CONTENT_CATEGORIES[1], 'pizza': self.CONTENT_CATEGORIES[1],
      'donut': self.CONTENT_CATEGORIES[1], 'cake': self.CONTENT_CATEGORIES[1],
      'potted plant': self.CONTENT_CATEGORIES[2],
      'frisbee': self.CONTENT_CATEGORIES[3], 'skis': self.CONTENT_CATEGORIES[3],
      'snowboard': self.CONTENT_CATEGORIES[3], 'sports ball': self.CONTENT_CATEGORIES[3],
      'kite': self.CONTENT_CATEGORIES[3], 'baseball bat': self.CONTENT_CATEGORIES[3],
      'baseball glove': self.CONTENT_CATEGORIES[3], 'skateboard': self.CONTENT_CATEGORIES[3],
      'surfboard': self.CONTENT_CATEGORIES[3], 'tennis racket': self.CONTENT_CATEGORIES[3],
      'person': self.CONTENT_CATEGORIES[4],
      'bicycle': self.CONTENT_CATEGORIES[5], 'car': self.CONTENT_CATEGORIES[5],
      'motorcycle': self.CONTENT_CATEGORIES[5], 'airplane': self.CONTENT_CATEGORIES[5],
      'bus': self.CONTENT_CATEGORIES[5], 'train': self.CONTENT_CATEGORIES[5],
      'truck': self.CONTENT_CATEGORIES[5], 'boat': self.CONTENT_CATEGORIES[5]
    }
    self.IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY = {
      'tbd': self.CONTENT_CATEGORIES[6]
    }

  def class_to_category(self, inference_type, class_name):
    """Converts result class from dataset to content category"""
    if inference_type == self.INFERENCE_TYPES[0] and class_name in self.OBJECT_DETECTION_CLASSES_TO_CATEGORY:
      return self.OBJECT_DETECTION_CLASSES_TO_CATEGORY[class_name]
    if inference_type == self.INFERENCE_TYPES[1] and class_name in self.IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY:
      return self.IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY[class_name]
    return None

  def get_inference_results(self, inference_type, model_name):
    """Calls torchserve inference api and returns response"""
    result_classes = []
    with urllib.request.urlopen(f'http://ml:5002/predictions/{model_name}') as url:
      data = json.loads(url.read().decode('utf-8'))
      if inference_type == self.INFERENCE_TYPES[0]:
        for item in data:
          keys = item.keys()
          if 'score' in keys and item['score'] > 0.90:
            result_classes.append(item[keys[0]])
        return result_classes
      if inference_type == self.INFERENCE_TYPES[1]:
        for item in data:
          if data[item] > 0.90:
            result_classes.append(item)
        return result_classes
    return result_classes

  def process(self):
    result_categories = []
    # make inference call for object detection
    od_classes = [''] # later(omkar): get object detection classes with 90% and above
    for od_class in od_classes:
      result_categories.append(self.class_to_category(self.INFERENCE_TYPES[0], od_class))

    # make inference call for image classification
    ic_classes = [''] # later(omkar): get image classification classes with 90% and above
    for ic_class in ic_classes:
      result_categories.append(self.class_to_category(self.INFERENCE_TYPES[1], ic_class))

    print(f'[things]: {result_categories}')    
