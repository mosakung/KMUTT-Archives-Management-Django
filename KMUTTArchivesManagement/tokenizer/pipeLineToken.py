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
import tensorflow as tf
from tokenizer.deepcut import deepcut


def pipeLineTokenizer(filename, fulltext):
    corpusInPage = []
    resultCorpusInPage = []
    physical_devices = tf.config.list_physical_devices('GPU')
    try:
        # Disable all GPUS
        tf.config.set_visible_devices([], 'GPU')
        visible_devices = tf.config.get_visible_devices()
        for device in visible_devices:
            assert device.device_type != 'GPU'
    except:
        #  Invalid device or cannot modify virtual devices once initialized.
        pass

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

    corpusMED = loadSpecific()

    for value in corpusInPage:
        word = spellCheckAuto(value)
        word = cleanDot(word)
        word = spellCheckSpecific(word, corpusMED)
        resultCorpusInPage.append(word)

    pageIndex = 0
    regexSearch = re.search(r'(?<=page-)\d+(?=.txt)', filename)

    if regexSearch != None:
        pageIndex = regexSearch.group(0)

    return {
        "pageIndex": pageIndex,
        "filename": filename,
        "rawKeywords": resultCorpusInPage
    }
