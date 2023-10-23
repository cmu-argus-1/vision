import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import models, transforms
from data_loader import CustomImageDataset
from plotter import Plotter


class ImageClassifier:
    def __init__(self, train_path, test_path, live_plot_flag, save_plot_flag, save_plot_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self._prepare_data(train_path, test_path)
        self._initialize_model()
        self.plotter = Plotter() 
        self.live_plot_flag = live_plot_flag
        self.save_plot_flag = save_plot_flag
        self.save_plot_path = save_plot_path

    def _prepare_data(self, train_path, test_path):
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        train_dataset = CustomImageDataset(root_dir=train_path, transform=transform)
        test_dataset = CustomImageDataset(root_dir=test_path, transform=transform)
        self.train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
        self.test_loader = DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)

    def _initialize_model(self):
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, len(self.train_loader.dataset.classes))
        self.model = self.model.to(self.device)

    def train(self, epochs=10, learning_rate=1e-3):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        for epoch in range(epochs):
            for batch_idx, (data, targets) in enumerate(self.train_loader):
                data = data.to(self.device)
                targets = targets.to(self.device)
                scores = self.model(data)
                loss = criterion(scores, targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
            if self.live_plot_flag:
                self.plotter.update_loss(loss.item()) 
            if self.save_plot_flag and epoch +1 == epochs:
                self.plotter.save_plot(self.save_plot_path)

    def save_model(self, path='model.pth'):
        torch.save(self.model.state_dict(), path)

    def load_model(self, path='model.pth'):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

    def evaluate(self):
        correct = 0
        total = 0
        with torch.no_grad():
            for data in self.test_loader:
                images, labels = data
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()


        print(f'Accuracy of the network on the test images: {100 * correct / total}%')
