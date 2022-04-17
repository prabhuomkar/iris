# ML Models

## Things
In order to use a custom model, you can refer two examples given below:
- [ResNet-152](things/resnet.py)
- [EfficientNet-B7](things/efficientnet.py)
Note: Both of these models are trained on imagenet, so you need `imagenet_classes.txt` for mapping result category ids to category names.

### Generate TorchScript Module and Move to Worker Checkpoints
- ResNet-152:
```
cd things
python3 resnet.py
mv things-model.pt ../../worker/checkpoints/things-model.pt
```
- EfficientNet-B7
```
cd things
python3 efficientnet.py
mv things-model.pt ../../worker/checkpoints/things-model.pt
```
