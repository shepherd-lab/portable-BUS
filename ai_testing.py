import sys
import time
import math
import torch
import numpy as np

import torchvision.models as m
import torchvision.transforms as T
from torchvision.transforms import v2
from torchvision.models.detection import fasterrcnn_mobilenet_v3_large_320_fpn, \
fasterrcnn_resnet50_fpn, retinanet_resnet50_fpn, ssdlite320_mobilenet_v3_large, ssd300_vgg16
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor


augsDL = [v2.PILToTensor(), v2.ToDtype(torch.float, scale=True), v2.ToPureTensor()]

# load in some model to test, see DemoModelTrainEval.ipynb for examples of other architectures 
model2 = fasterrcnn_resnet50_fpn()
num_classes = 2  # 1 class (lesion) + background
in_features = model2.roi_heads.box_predictor.cls_score.in_features
model2.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
model2.load_state_dict(torch.load('fasterrcnn_resnet50_fpn.pth', map_location=torch.device('cpu')))
model2.eval()

def predict_with_model(pil_image):
    test_augs = v2.Compose(augsDL)
    try: 
        augmented_im = test_augs(pil_image)
        output2 = model2([augmented_im])
    except Exception as e:
        print('exception: ', e)
        sys.exit(1)
    return output2

def test_augmentations(pil_image):
    test_augs = v2.Compose(augsDL)
    try: 
        test_augs(pil_image)
    except Exception as e:
        print(e)
        sys.exit(1)
    return "1"
