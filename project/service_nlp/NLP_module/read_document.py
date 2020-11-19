import os


def read(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read().splitlines()
    return False


def readDirectory(path):
    result = {}

    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            data = read(filename)
            result.update({name: data})
        for name in directories:
            print(os.path.join(root, name))

    return result
