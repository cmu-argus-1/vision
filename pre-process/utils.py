import os
def check_dir(dir_path, create=False):
    if not os.path.exists(dir_path):
        if create:
            os.makedirs(dir_path)
            print('Create directory: {}'.format(dir_path))
        else:
            # Error message
            print('Directory not found: {}'.format(dir_path))
