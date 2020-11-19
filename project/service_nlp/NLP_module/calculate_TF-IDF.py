import math


def TF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bowCount)
    return tfDict


def logTF(wordDict):
    tfDict = {}
    for word, count in wordDict.items():
        if count == 0:
            tfDict[word] = 0
        else:
            tfDict[word] = 1 + math.log10(count)
    return tfDict


def doubleTF(wordDict, bow):
    K = 0.4
    maxDict = 0
    tfDict = {}
    for word, count in wordDict.items():
        if maxDict < count:
            maxDict = count

    for word, count in wordDict.items():
        tfDict[word] = K + (1 - K) * (count / maxDict)

    return tfDict


def IDF(docList):
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))

    return idfDict


def smoothIDF(docList):
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / (1 + float(val))) + 1

    return idfDict


def maxIDF(docList):
    idfDict = {}
    maxDict = 0
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, count in idfDict.items():
        if maxDict < count:
            maxDict = count

    for word, val in idfDict.items():
        idfDict[word] = math.log10(float(maxDict) / (1 + float(val)))

    return idfDict


def probabilisticIDF(docList):
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        if((N - float(val)) / float(val) == 0):
            idfDict[word] = 0
        else:
            idfDict[word] = math.log10((N - float(val)) / float(val))

    return idfDict


def TFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf
