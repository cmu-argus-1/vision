import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image
import yaml
import matplotlib.pyplot as plt
from regressor import ImageRegressor

if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    regressor = ImageRegressor(config)
    if config['flags']['train_flag']:
        regressor.train()
        regressor.save_model(path=config['paths']['model_save_path'])
    else:
        regressor.load_model(path=config['paths']['model_load_path'])
    
    regressor.evaluate()
