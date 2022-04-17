import torch
import torchvision

class IRISThingsClassifierModule(torch.nn.Module):
  def __init__(self):
    super(IRISThingsClassifierModule, self).__init__()
    self.model = torchvision.models.efficientnet_b7(pretrained=True)
    self.model.eval()
    with open('imagenet_classes.txt', 'r') as f:
      self.categories = [s.strip() for s in f.readlines()]

  def forward(self, input):
    output = self.model(input)
    probabilities = torch.nn.functional.softmax(output, dim=1)
    top_prob, top_catid = torch.topk(probabilities, 1)
    return self.categories[top_catid[0].item()] if top_prob[0].item() > 0.85 else None

if __name__ == '__main__':
  scripted_module = torch.jit.script(IRISThingsClassifierModule())
  scripted_module.save('things-model.pt')
