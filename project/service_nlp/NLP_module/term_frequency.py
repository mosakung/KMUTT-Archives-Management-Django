import math


def logTF(wordDict):
    tfDict = {}
    for word, count in wordDict.items():
        if count == 0:
            tfDict[word] = 0
        else:
            tfDict[word] = math.log10(1 + count)
    return tfDict
