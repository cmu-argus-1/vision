import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import models, transforms
from torchvision.models import resnet18, ResNet18_Weights
from data_loader import CustomImageDataset
from plotter import Plotter


class ImageRegressor:
    def __init__(self, config):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.live_plot_flag = config['flags']['live_plot_flag']
        self.save_plot_flag = config['flags']['save_plot_flag']
        self.save_plot_path = config['paths']['save_plot_path']
        self.resize_shape = [int(config['resize_shape']['height']), int(config['resize_shape']['width'])]
        self.learning_rate = float(config['learning_rate'])
        self.epochs = config['epochs']
        self._prepare_data(config['paths']['train_path'], config['paths']['test_path'])
        self._initialize_model()
        self.plotter = Plotter() 

    def _prepare_data(self, train_path, test_path):
        transform = transforms.Compose([
            transforms.Resize((self.resize_shape[0], self.resize_shape[1])),
            transforms.ToTensor(),
        ])
        train_dataset = CustomImageDataset(root_dir=train_path, transform=transform)
        test_dataset = CustomImageDataset(root_dir=test_path, transform=transform)
        self.train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
        self.test_loader = DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)

    def _initialize_model(self):
        self.model = resnet18(weights=ResNet18_Weights.DEFAULT) 
        self.model.fc = nn.Linear(self.model.fc.in_features, len(self.train_loader.dataset.labels[0]))
        self.model = self.model.to(self.device)

    def train(self):
        criterion = nn.MSELoss()    
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        for epoch in range(self.epochs):
            for batch_idx, (data, targets) in enumerate(self.train_loader):
                data = data.to(self.device)
                targets = targets.to(self.device)
                scores = self.model(data)
                loss = criterion(scores, targets.float())   
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            print(f'Epoch [{epoch+1}/{self.epochs}], Loss: {loss.item():.4f}')
            if self.live_plot_flag:
                self.plotter.update_loss(loss.item()) 
            if self.save_plot_flag and epoch +1 == self.epochs:
                self.plotter.save_plot(self.save_plot_path)

    def save_model(self, path='model.pth'):
        torch.save(self.model.state_dict(), path)

    def load_model(self, path='model.pth'):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

    def evaluate(self):
        mse_loss = nn.MSELoss() 
        total_mse_loss = 0.0
        total_samples = 0

        with torch.no_grad():
            for data in self.test_loader:
                images, targets = data
                images, targets = images.to(self.device), targets.to(self.device)
                outputs = self.model(images)
                # print(outputs, targets)
                batch_loss = mse_loss(outputs, targets.float())
                total_mse_loss += batch_loss.item()
                total_samples += len(targets)

        mean_mse_loss = total_mse_loss / total_samples
        print(f'Loss of the network on the test images: {mean_mse_loss:.4f}')
        return mean_mse_loss


        
