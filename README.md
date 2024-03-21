# Assessing the Feasibility of AI-Enhanced Portable Ultrasound for Improved Breast Cancer Early Detection in Remote Areas
###### Github repository containing all relevant code for 17th International Workshop on Breast Imaging 2024 submission

This repository contains AI model training and evaluation code, as well as labeled ultrasound phantom data used for experiments in _Assessing the Feasibility of AI-Enhanced Portable Ultrasound for Improved Breast Cancer Early Detection in Remote Areas_. Model timing code was developed on top of [https://github.com/clariusdev/cast], and all logic for streaming images from Clarius devices can be found in that repository.

## Installation and system requirements
- Tested on CentOS Linux 7 (Core)
- Python version: 3.8.10

## Demo
- Notebooks demonstrating model training and evaluation are provided in the notebooks folder.
- Helper functions referenced in provided demonstration notebooks can be downloaded from [Torchvision](https://github.com/pytorch/vision/tree/main/gallery/). 
- To validate code functionality, run sample code in notebook corresponding to desired functionality (e.g. model_loading.ipynb for an example of how to load and test pretrained models)

## Dataset 
All phantom data used for model training and evaluation in _Assessing the Feasibility of AI-Enhanced Portable Ultrasound for Improved Breast Cancer Early Detection in Remote Areas_ can be accessed through the provided Google Drive link: [Access Data](https://drive.google.com/drive/folders/1GEfqTNpqRxtoa7ZFWf0sUR2UEEZBNHkk?usp=sharing).
  
In this Google Drive, you will find the following resources:
  
- **Weights**: weights for FasterRCNN+MobileNetV3, FasterRCNN+ResNet50, RetinaNet+ResNet50, SSD+VGG16, and SSDLite+MobileNetV3 architectures inlcuded in our analysis and timing trials, pretrained on ultrasound phantom data.
- **Videos**: video clips of ultrasound phantom scans used to generate training, validation and testing data for AI model development.
- **Labeled Video Data**: json files containing lesion location annotations.
- **Frames**: individual frames extracted from the video clips.

## Citation 

## Accessing the Data



