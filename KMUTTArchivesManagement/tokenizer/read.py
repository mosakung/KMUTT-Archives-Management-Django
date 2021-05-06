import os


def readfile(path):
    with open(path, "r", encoding="utf8") as f:
        line = f.read().splitlines()
        arrayWord = []
        for words in line:
            word = words.split()
            arrayWord.extend(word)
        return arrayWord
    return False


def readDirectory(path):
    result = {}

    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            data = readfile(filename)
            print(data)
            result.update({name: data})
        for name in directories:
            print(os.path.join(root, name))

    return result
