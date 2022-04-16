if [ -f "resnet152.pth" ]; then
  echo "resnet152.pth exists"
else
  echo "downloading resnet152.pth"
  curl https://download.pytorch.org/models/resnet152-394f9c45.pth --output ./resnet152.pth
fi
if [ -f "imagenet_classes.txt" ]; then
  echo "imagenet_classes.txt exists"
else
  echo "downloading imagenet_classes.txt"
  curl https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt --output ./imagenet_classes.txt
fi