if [ -f "checkpoints/things-model.pt" ]; then
  echo "things-model.pth exists"
else
  echo "downloading things-model.pt"
  curl https://download.pytorch.org/models/resnet152-394f9c45.pth --output ./checkpoints/things-model.pt
fi
if [ -f "checkpoints/things-model-result-mapping.txt" ]; then
  echo "things-model-result-mapping.txt exists"
else
  echo "downloading things-model-result-mapping.txt"
  curl https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt --output ./checkpoints/things-model-result-mapping.txt
fi
if [ -f "checkpoints/20180402-114759-vggface2.pt" ]; then
  echo "20180402-114759-vggface2.pt exists"
else
  echo "downloading 20180402-114759-vggface2.pt"
  curl https://github.com/timesler/facenet-pytorch/releases/download/v2.2.9/20180402-114759-vggface2.pt --output ./checkpoints/20180402-114759-vggface2.pt
fi