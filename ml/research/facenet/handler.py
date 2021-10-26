from facenet_pytorch import MTCNN, InceptionResnetV1
from ts.torch_handler.vision_handler import VisionHandler


class FaceNetHandler(VisionHandler):
  """FaceNet Handler"""
  def __init__(self):
    super(FaceNetHandler, self).__init__()
    self.initialized = False

  def initialize(self, ctx):
    """Initialize FaceNetHandler"""
    self.manifest = ctx.manifest

    self.mtcnn = MTCNN()
    self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

  def inference(self, data):
    # pass through mtcnn model to get face probs
    # calcuate and return image embeddings
    return NotImplementedError

  def postprocess(self, data):
    # clustering based on embeddings
    return NotImplementedError
