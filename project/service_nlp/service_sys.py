from threading import Thread
from service_nlp.NLP_module import read_document
from service_nlp.NLP_module import cut_word
from service_nlp.NLP_module import clean_token
from service_nlp.NLP_module import spell_check
from service_nlp.NLP_module import stemming
from service_nlp.NLP_module import create_unique
from service_nlp.NLP_module import create_frame
from service_nlp.NLP_module import term_frequency
from service_nlp.NLP_module import load_config
from service_nlp.NLP_module import clean_stop_word
from service_nlp.NLP_module import normalize
import concurrent.futures as cf
from itertools import repeat


def initTF(directoryName):
    list_word_extend = []

    ''' Read document with (read directory) '''
    pathRead = './document' + directoryName
    documents = read_document.readDirectory(pathRead)

    def childTokenizer(value, key):
        paramCut = []
        print(key + '-> start')
        for x in value:
            ''' deepcut '''
            precut = cut_word.cut(x)

            ''' clean token '''
            precut_filter_space = list(
                map(clean_token.delete_space_regex, precut))
            precut_filter_space_unnecessary_words = clean_token.delete_unnecessary_words(
                precut_filter_space)

            ''' extend to array (THREAD) result '''
            paramCut.extend(precut_filter_space_unnecessary_words)

        ''' pyspellcheck '''
        paramCut = list(map(spell_check.spellCheckEnTh, paramCut))

        """ Normalize """
        paramCut = list(map(normalize.clean_dot, paramCut))

        ''' specific spellcheck '''
        terms_specific = load_config.load_specific()
        paramCut = list(
            map(spell_check.spellcheck_specific_term, paramCut, repeat(terms_specific)))

        """ stopcut delete """
        paramCut = list(filter(clean_stop_word.filter_stop_word, paramCut))

        ''' extend to array (JOIN THREAD) result '''
        list_word_extend.extend(paramCut)
        print(key + '-> end')

    ''' Thread limit task '''
    with cf.ThreadPoolExecutor(max_workers=5) as executor:
        for key, value in documents.items():
            executor.submit(childTokenizer, value, key)

    ''' Basic for loop '''
    # for key, value in documents.items():
    #     childTokenizer(value, key)

    ''' stemming term '''
    list_word_extend = list(map(stemming.lemmatizer, list_word_extend))

    ''' calculate TF '''
    unique = create_unique.unique(list_word_extend)
    documentsFreq = create_frame.createFrame(list_word_extend, unique)
    tf = term_frequency.logTF(documentsFreq)

    return tf


def error_validate_frequency(log):
    ''' 
    this function check insert term row more than one in term table
    if have some row update or insert more than 1 frequency
    return error term (NAME)
    '''
    error_log = {}
    for key, value in log.items():
        if value > 1:
            error_log.update({key: value})

    if error_log == {}:
        return False

    return error_log
