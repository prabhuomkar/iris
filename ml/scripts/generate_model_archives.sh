# generate maskrcnn model archive
if [ -f "models/maskrcnn.mar" ]; then
  echo "maskrcnn.mar exists"
else
  echo "generating maskrcnn.mar"
  torch-model-archiver --model-name maskrcnn --version 1.0 --model-file ./research/maskrcnn/model.py --serialized-file ./models/maskrcnn.pth --handler ./research/maskrcnn/handler.py --extra-files ./research/maskrcnn/index_to_name.json
  mv maskrcnn.mar ./models
fi
# generate resnet152 model archive
if [ -f "models/resnet152.mar" ]; then
  echo "resnet152.mar exists"
else
  echo "generating resnet152.mar"
  torch-model-archiver --model-name resnet152 --version 1.0 --model-file ./research/resnet152/model.py --serialized-file ./models/resnet152.pth --handler ./research/resnet152/handler.py --extra-files ./research/resnet152/index_to_name.json
  mv resnet152.mar ./models
fi