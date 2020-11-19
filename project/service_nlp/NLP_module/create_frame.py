def createFrame(listWord, listUnique):
    keyFrame = dict.fromkeys(listUnique, 0)

    for word in listWord:
        keyFrame[word] += 1

    return keyFrame
