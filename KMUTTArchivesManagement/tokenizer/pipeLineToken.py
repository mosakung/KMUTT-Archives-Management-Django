from tokenizer.stopword import filterStopword
from tokenizer.lemmatizer import *
from itertools import repeat
from tokenizer.loadConfig import loadSpecific
from tokenizer.normalize import *
from tokenizer.spellCheck import *
from tokenizer.cleanToken import *
from tqdm import tqdm
from tokenizer.read import *
from tokenizer.deepcut import deepcut
from multiprocessing import Pool, current_process
import tensorflow as tf


def pipeLineTokenizer(filename, fulltext):
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        # Create 2 virtual GPUs with 1GB memory each
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices(
                    'GPU')
        except RuntimeError as e:
            # Virtual devices must be set before GPUs have been initialized
            print(e)
    if(current_process().name == "SpawnPoolWorker-4"):
        position = 0
    elif(current_process().name == "SpawnPoolWorker-5"):
        position = 1
    elif(current_process().name == "SpawnPoolWorker-6"):
        position = 2
    elif(current_process().name == "SpawnPoolWorker-7"):
        position = 3
    elif(current_process().name == "SpawnPoolWorker-8"):
        position = 4

    textDeepcut = '[SLOT:{position}]{filename}(Deepcut)'.format(
        position=position,
        filename=filename
    )
    textTokenize = '[SLOT:{position}]{filename}(Tokenize)'.format(
        position=position,
        filename=filename
    )
    textDone = '{filename}'.format(
        filename=filename
    )

    corpusInPage = []
    resultCorpusInPage = []

    with tqdm(
        position=position,
        total=len(fulltext),
        desc=textDeepcut,
        ascii=True,
        ncols=130,
        leave=False,
        disable=True,
    ) as pbarDeepcut:
        for line in fulltext:
            # Deep Cut process
            token = deepcut(line)
            # clean token
            token = list(map(delete_space, token))
            token = list(map(delete_latin, token))
            token = list(filter(delete_unnecessary_words, token))
            token = list(map(to_lower_case, token))
            # push to corpus
            corpusInPage.extend(token)
            pbarDeepcut.update()
        pbarDeepcut.clear()

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

    with tqdm(
        position=position,
        total=len(corpusInPage),
        desc=textTokenize,
        ascii=True,
        ncols=130,
        leave=True,
        disable=True,
    ) as pbarTokenize:
        for value in corpusInPage:
            word = spellCheckAuto(value)
            word = cleanDot(word)
            word = spellCheckSpecific(word, corpusMED)
            resultCorpusInPage.append(word)
            pbarTokenize.update()
        pbarTokenize.set_description(textDone)
        pbarTokenize.clear()

    pageIndex = 0
    regexSearch = re.search(r'(?<=page-)\d+(?=.txt)', filename)

    if regexSearch != None:
        pageIndex = regexSearch.group(0)

    return {
        "pageIndex": pageIndex,
        "filename": filename,
        "rawKeywords": resultCorpusInPage
    }
