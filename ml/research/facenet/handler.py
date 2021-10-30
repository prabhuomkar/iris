import os
import io
import uuid
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from ts.torch_handler.base_handler import BaseHandler


class FaceDetector(BaseHandler):
  """FaceNet Handler"""
  def __init__(self):
    super(FaceDetector, self).__init__()
    self.mtcnn_model = None
    self.resnet_model = None
    self.initialized = False

  def initialize(self, context):
    """Initialize FaceNetHandler"""
    self.manifest = context.manifest

    self.mtcnn_model = MTCNN(margin=32, image_size=240, keep_all=True)
    self.resnet_model = InceptionResnetV1(pretrained='vggface2').eval()
    self.initialized = True

  def preprocess(self, data):
    for row in data:
      image = row.get('data') or row.get('body')
      if isinstance(image, (bytearray, bytes)):
        image = Image.open(io.BytesIO(image))
      return image

  def inference(self, data, *args, **kwargs):
    filename = uuid.uuid4()
    res_bytes = []
    ten_imgs = []
    imgs = self.mtcnn_model(data, save_path=f'{filename}.jpg')
    result = []
    if imgs is not None:
      for i in range(1, len(imgs)+1):
        ten_imgs.append(imgs[i-1])
        img_path = f'{filename}.jpg' if i == 1 else f'{filename}_{i}.jpg'
        with open(img_path, 'rb') as f:
          res_bytes.append(f.read())
          os.remove(img_path)
      stacked_imgs = torch.stack(ten_imgs) # pylint: disable=no-member
      embeddings = self.resnet_model(stacked_imgs)
      result = [
        { 'data': res.decode('latin1'), 'embedding': embed.tolist() } for res, embed in zip(res_bytes, embeddings)
      ]
    return result

  def postprocess(self, data):
    return [data]
