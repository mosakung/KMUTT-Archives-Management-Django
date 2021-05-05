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

import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(processName)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    filename='F:\Ty\project kmutt\KMUTT-Archives-Management-Django\KMUTTArchivesManagement\processLog.log',
                    filemode='a')

def pipeLineTokenizer(filename, fulltext):
    corpusInPage = []
    resultCorpusInPage = []
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices(
                    'GPU')
                print(len(gpus), "Physical GPUs,", len(
                    logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

    logging.info("deepcut FileName: " + str(filename) + " start")
    
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
    logging.info("deepcut FileName: " + str(filename) + " finish")
    logging.info("spellCheckAuto FileName: " + str(filename) + " start")

    for value in corpusInPage:
        word = spellCheckAuto(value)
        word = cleanDot(word)
        word = spellCheckSpecific(word, corpusMED)
        resultCorpusInPage.append(word)

    pageIndex = 0
    regexSearch = re.search(r'(?<=page-)\d+(?=.txt)', filename)
    if regexSearch != None:
        pageIndex = regexSearch.group(0)
    logging.info("spellCheckAuto FileName: " + str(filename) + " finish")
    logging.info("PipeLineTokenizer FileName: " + str(filename) + " finish")
    return {
        "pageIndex": pageIndex,
        "filename": filename,
        "rawKeywords": resultCorpusInPage
    }
