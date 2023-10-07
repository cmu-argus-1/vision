import matplotlib.pyplot as plt

class Plotter:
    def __init__(self):
        self.loss_history = []

    def update_loss(self, loss):
        self.loss_history.append(loss)
        self.plot_loss()

    def plot_loss(self):
        plt.plot(self.loss_history, label='Training Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Loss vs. Epoch')
        plt.draw()
        plt.pause(0.001)

    def save_plot(self, file_path='loss_plot.png'):
        plt.savefig(file_path)
        print(f'Loss plot saved at {file_path}')
