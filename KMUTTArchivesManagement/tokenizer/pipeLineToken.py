from threading import Lock
import threading
from multiprocessing import Pool, current_process, Manager
from tokenizer.stopword import filterStopword
from tokenizer.lemmatizer import *
import re
from itertools import repeat
from tokenizer.loadConfig import loadSpecific
from tokenizer.normalize import *
from tokenizer.spellCheck import *
from tokenizer.cleanToken import *
import concurrent.futures as cf
from tqdm import tqdm
from threading import Thread
from tokenizer.read import *
from tokenizer.deepcut import deepcut
import tensorflow as tf


def pipeLineTokenizer(filename, fulltext):
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        # Restrict TensorFlow to only use the first GPU
        try:
            tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,",
                  len(logical_gpus), "Logical GPU")
        except RuntimeError as e:
            # Visible devices must be set before GPUs have been initialized
            print(e)
    # if(current_process().name == "SpawnPoolWorker-4"):
    #     position = 0
    # elif(current_process().name == "SpawnPoolWorker-5"):
    #     position = 1
    # elif(current_process().name == "SpawnPoolWorker-6"):
    #     position = 2
    # elif(current_process().name == "SpawnPoolWorker-7"):
    #     position = 3
    # elif(current_process().name == "SpawnPoolWorker-8"):
    #     position = 4

    # textDeepcut = '[SLOT:{position}]{filename}(Deepcut)'.format(
    #     position=position,
    #     filename=filename
    # )
    # textTokenize = '[SLOT:{position}]{filename}(Tokenize)'.format(
    #     position=position,
    #     filename=filename
    # )
    # textDone = '{filename}'.format(
    #     filename=filename
    # )

    corpusInPage = []
    resultCorpusInPage = []

    # with tqdm(
    #     position=position,
    #     total=len(fulltext),
    #     desc=textDeepcut,
    #     ascii=True,
    #     ncols=130,
    #     leave=False,
    #     disable=False,
    # ) as pbarDeepcut:
    for line in fulltext:
        # Deep Cut process
        token = deepcut(line)
        # clean token
        token = list(map(delete_space, token))
        token = list(map(delete_latin, token))
        token = list(filter(delete_unnecessary_words, token))
        while("" in token):
            token.remove("")
        token = list(map(to_lower_case, token))
        # push to corpus
        corpusInPage.extend(token)
        #     pbarDeepcut.update()
        # pbarDeepcut.clear()

    # # pyspell check
    # corpusInPage = list(map(spellCheckAuto, corpusInPage))
    # # Normalize
    # corpusInPage = list(map(cleanDot, corpusInPage))
    # # specific spellcheck
    # corpusMED = loadSpecific()
    # corpusInPage = list(
    #     map(spellCheckSpecific, corpusInPage, repeat(corpusMED))
    # )

    corpusMED = loadSpecific()

    # with tqdm(
    #     position=position,
    #     total=len(corpusInPage),
    #     desc=textTokenize,
    #     ascii=True,
    #     ncols=130,
    #     leave=True,
    #     disable=False,
    # ) as pbarTokenize:
    for value in corpusInPage:
        word = spellCheckAuto(value)
        word = cleanDot(word)
        word = spellCheckSpecific(word, corpusMED)
        resultCorpusInPage.append(word)
        # pbarTokenize.update()
        # pbarTokenize.set_description(textDone)
        # pbarTokenize.clear()

    pageIndex = 0
    regexSearch = re.search(r'(?<=page-)\d+(?=.txt)', filename)

    if regexSearch != None:
        pageIndex = regexSearch.group(0)

    return {
        "pageIndex": pageIndex,
        "filename": filename,
        "rawKeywords": resultCorpusInPage
    }
