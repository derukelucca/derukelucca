import os

def get_file_paths(directory):
    file_paths = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    
    return file_paths

directory = '/path/to/your/directory'
paths = get_file_paths(directory)

for path in paths:
    print(path)
