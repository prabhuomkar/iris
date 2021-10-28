from ts.torch_handler.object_detector import ObjectDetector as PObjectDetector
from ts.utils.util import map_class_to_label


class ObjectDetector(PObjectDetector):
  """Object Detector"""
  OBJECT_DETECTION_CLASSES_TO_CATEGORY = {
    'bird': 'ANIMALS', 'cat': 'ANIMALS',
    'dog': 'ANIMALS', 'horse': 'ANIMALS',
    'sheep': 'ANIMALS', 'cow': 'ANIMALS',
    'elephant': 'ANIMALS', 'bear': 'ANIMALS',
    'zebra': 'ANIMALS', 'giraffe': 'ANIMALS',
    'banana': 'FOOD', 'apple': 'FOOD',
    'sandwich': 'FOOD', 'orange': 'FOOD',
    'broccoli': 'FOOD', 'carrot': 'FOOD',
    'hot dog': 'FOOD', 'pizza': 'FOOD',
    'donut': 'FOOD', 'cake': 'FOOD',
    'potted plant': 'GARDENS',
    'frisbee': 'SPORT', 'skis': 'SPORT',
    'snowboard': 'SPORT', 'sports ball': 'SPORT',
    'kite': 'SPORT', 'baseball bat': 'SPORT',
    'baseball glove': 'SPORT', 'skateboard': 'SPORT',
    'surfboard': 'SPORT', 'tennis racket': 'SPORT',
    'person': 'PEOPLE',
    'bicycle': 'TRAVEL', 'car': 'TRAVEL',
    'motorcycle': 'TRAVEL', 'airplane': 'TRAVEL',
    'bus': 'TRAVEL', 'train': 'TRAVEL',
    'truck': 'TRAVEL', 'boat': 'TRAVEL',
    'traffic light': 'CITYSCAPES', 'fire hydrant': 'CITYSCAPES',
    'street sign': 'CITYSCAPES', 'stop sign': 'CITYSCAPES',
    'parking meter': 'CITYSCAPES', 'bench': 'CITYSCAPES',
    'hat': 'UTILITY', 'backpack': 'UTILITY',
    'umbrella': 'UTILITY', 'shoe': 'UTILITY',
    'eye glasses': 'UTILITY', 'handbag': 'UTILITY',
    'tie': 'UTILITY', 'suitcase': 'UTILITY',
    'bottle': 'FOOD', 'plate': 'FOOD',
    'wine glass': 'FOOD', 'cup': 'FOOD',
    'fork': 'FOOD', 'knife': 'FOOD',
    'spoon': 'FOOD', 'bowl': 'FOOD',
    'chair': 'UTILITY', 'couch': 'HOUSES',
    'mirror': 'HOUSES', 'dining table': 'HOUSES',
    'window': 'HOUSES', 'desk': 'HOUSES',
    'toilet': 'HOUSES', 'door': 'HOUSES',
    'tv': 'UTILITY', 'laptop': 'UTILITY',
    'mouse': 'UTILITY', 'remote': 'UTILITY',
    'keyboard': 'UTILITY', 'phone': 'UTILITY',
    'microwave': 'UTILITY', 'oven': 'UTILITY',
    'toaster': 'UTILITY', 'sink': 'UTILITY',
    'refrigerator': 'UTILITY', 'blender': 'UTILITY',
    'book': 'UTILITY', 'clock': 'UTILITY',
    'vase': 'UTILITY', 'scissors': 'UTILITY',
    'drier': 'UTILITY', 'bed': 'HOUSES',
    'toothbrush': 'UTILITY', 'hair brush': 'UTILITY'
  }
  def postprocess(self, data):
    # get results from pytorch inferencing
    result = []
    box_filters = [row['scores'] >= self.threshold for row in data]
    filtered_boxes, filtered_classes, filtered_scores = [
        [row[key][box_filter].tolist() for row, box_filter in zip(data, box_filters)]
        for key in ['boxes', 'labels', 'scores']
    ]
    for classes, boxes, scores in zip(filtered_classes, filtered_boxes, filtered_scores):
        retval = []
        for _class, _box, _score in zip(classes, boxes, scores):
            _retval = map_class_to_label([[_box]], self.mapping, [[_class]])[0]
            _retval['score'] = _score
            retval.append(_retval)
        result.append(retval)
    # customizing based on skim requirements
    result = result[0]
    result_classes = []
    content_categories = []
    max_prob_found = False
    data = list(sorted(result, key=lambda x: x['score'], reverse=True))
    for i, elem in enumerate(data):
      keys = list(elem.keys())
      if 'score' in keys and elem['score'] > 0.80:
        result_classes.append(keys[0])
        if elem['score'] > 0.95:
          max_prob_found = True
      elif max_prob_found:
        break
      if i == 2: # in future, configure with topK sent via request
        break
    for od_class in result_classes:
      category = self.OBJECT_DETECTION_CLASSES_TO_CATEGORY[od_class]
      if category not in content_categories:
        content_categories.append(category)
    return [{
      "content_categories": content_categories,
      "classes": result_classes
    }]
