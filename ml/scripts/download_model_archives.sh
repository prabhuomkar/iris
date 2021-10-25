# object detection model
if [ -f "models/maskrcnn.mar" ]; then
  echo "maskrcnn.mar exists"
else
  echo "downloading maskrcnn.mar"
  curl https://torchserve.pytorch.org/mar_files/maskrcnn.mar --output ./models/maskrcnn.mar
fi
# image classification model
if [ -f "models/resnet152.mar" ]; then
  echo "resnet152.mar exists"
else
  echo "downloading resnet152.mar"
  curl https://torchserve.pytorch.org/mar_files/resnet-152-scripted_v2.mar --output ./models/resnet152.mar
fi
