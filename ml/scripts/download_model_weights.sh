# object detection model
if [ -f "models/maskrcnn.pth" ]; then
  echo "maskrcnn.pth exists"
else
  echo "downloading maskrcnn.pth"
  curl https://download.pytorch.org/models/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth --output ./models/maskrcnn.pth
fi
# image classification model
if [ -f "models/resnet152.pth" ]; then
  echo "resnet152.pth exists"
else
  echo "downloading resnet152.pth"
  curl https://download.pytorch.org/models/resnet152-394f9c45.pth --output ./models/resnet152.pth
fi
