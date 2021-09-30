torchserve --start --ts-config config.properties \
  --model-store models \
  --models maskrcnn=maskrcnn.mar resnet152=resnet152.mar 