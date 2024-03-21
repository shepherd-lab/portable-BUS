# Assessing the Feasibility of AI-Enhanced Portable Ultrasound for Improved Breast Cancer Early Detection in Remote Areas
###### Github repository containing all relevant code for 17th International Workshop on Breast Imaging 2024 submission

This repository contains AI model training and evaluation code, as well as labeled ultrasound phantom data used for experiments in _Assessing the Feasibility of AI-Enhanced Portable Ultrasound for Improved Breast Cancer Early Detection in Remote Areas_. Model timing code was developed on top of the open-source [Clarius Cast API] (https://github.com/clariusdev/cast), and all logic for streaming images from Clarius devices can be found in that repository. We provide minimal examples which can be integrated into the Cast API, but do not reproduce their work here.  

## Installation and system requirements
###### Model training
- Tested on CentOS Linux 7 (Core)
- Python version: 3.10.12
- Torchvision=0.17.1
- PIL=9.4.0
  
###### Model timing and prediction display during scanning 
- Tested on Windows 11 Pro 23H2
- Python version: 3.11.5
- Pyside6=6.6.1
- Torchvision=0.17.1
- Clarius Cast API=11.1.0
- PIL=9.4.0

## Demo
- Notebook demonstrating model training and evaluation is provided in `DemoModelTrainEval.ipynb`.
- Scripts which can be used with the Clarius Cast API are provided, `pysidecaster.py` (slight modifications from the version provided by the Cast API to allow for drawing of AI model prediction overlay) and `ai_testing.py` (for generating model predictions from finetuned architectures).  
- Helper functions referenced in provided demonstration notebook can be downloaded from [Torchvision](https://github.com/pytorch/vision/tree/main/gallery/). 
- To validate code functionality, run sample code corresponding to desired functionality.

## Dataset 
All phantom data used for model training and evaluation in _Assessing the Feasibility of AI-Enhanced Portable Ultrasound for Improved Breast Cancer Early Detection in Remote Areas_ can be accessed through the provided Google Drive link: [Access Data](https://drive.google.com/drive/folders/1GEfqTNpqRxtoa7ZFWf0sUR2UEEZBNHkk?usp=sharing).
  
In this Google Drive, you will find the following resources:
  
- **Weights**: weights for FasterRCNN+MobileNetV3, FasterRCNN+ResNet50, RetinaNet+ResNet50, SSD+VGG16, and SSDLite+MobileNetV3 architectures inlcuded in our analysis and timing trials, pretrained on ultrasound phantom data.
- **Videos**: video clips of ultrasound phantom scans used to generate training, validation and testing data for AI model development.
- **Labeled Video Data**: json files containing lesion location annotations.
- **Frames**: individual frames extracted from the video clips.

## Citation 
TODO
