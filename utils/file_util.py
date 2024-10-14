import os


def get_filenames(folder_path, type=".csv"):
    for filename in os.listdir(folder_path):
        if filename.endswith(type):
            yield os.path.join(folder_path, filename)


def read_binary(path):
    with open(path, "rb") as f:
        return f.read()
    return False


def save_binary(path, data, encode=None):
    with open(path, "wb") as f:
        if encode:
            data = data.encode(encode)
        return f.write(data)
    return False