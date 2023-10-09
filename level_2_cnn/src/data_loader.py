import os
from PIL import Image
from torch.utils.data import Dataset
from utils import find_label
import torch
class CustomImageDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = os.listdir(root_dir)
        self.files = []
        self.labels = []
        for class_i in self.classes:
            curr_class_path = os.path.join(root_dir, class_i)
            for f in os.listdir(curr_class_path):
                f_path = os.path.join(curr_class_path, f)
                if f.endswith('.jpg'):
                    rgb_image = Image.open(f_path).convert('RGB')
                    if self.transform:
                        rgb_image = self.transform(rgb_image)
                    self.files.append(rgb_image)
                if f.endswith('.txt'):
                    self.labels.append(torch.tensor([float(find_label(f_path, 'SUN_AZIMUTH')), float(find_label(f_path, 'SUN_ELEVATION'))], dtype=torch.float32)) 


    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        return self.files[idx], self.labels[idx]

