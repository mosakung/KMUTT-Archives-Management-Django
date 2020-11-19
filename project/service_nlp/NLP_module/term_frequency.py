import math

def logTF(wordDict):
    tfDict = {}
    for word, count in wordDict.items():
        if count == 0:
            tfDict[word] = 0
        else:
            tfDict[word] = 1 + math.log10(count)
    return tfDict
