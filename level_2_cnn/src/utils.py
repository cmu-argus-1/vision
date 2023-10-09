import os

def find_label(file_path, label_name):
    file_data = open(file_path, 'r')
    for line in file_data:
        if label_name in line:
            return line.split(label_name)[1][2:].strip()
    file_data.close()
