from threading import Thread
import re
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
from service_nlp import service_db as sdb


def initialize_PRE_keyword(directoryName, doc_id):
    ''' defind GOLBAL '''
    page_set = []
    ''' Read document with (read directory) '''
    pathRead = './document' + directoryName
    documents = read_document.readDirectory(pathRead)

    def main(key, value_arr):
        raw_keyword = []
        ''' loop line in document '''
        for value in value_arr:
            ''' deepcut '''
            process = cut_word.cut(value)

            ''' clean token '''
            process = list(map(clean_token.delete_space_regex, process))
            process = clean_token.delete_unnecessary_words(process)

            ''' extend to raw_keyword '''
            raw_keyword.extend(process)

        ''' pyspellcheck '''
        # raw_keyword = list(map(spell_check.spellCheckEnTh, raw_keyword))

        """ Normalize """
        raw_keyword = list(map(normalize.clean_dot, raw_keyword))

        ''' specific spellcheck '''
        terms_specific = load_config.load_specific()
        raw_keyword = list(
            map(spell_check.spellcheck_specific_term, raw_keyword, repeat(terms_specific)))

        """ stopcut delete """
        raw_keyword = list(
            filter(clean_stop_word.filter_stop_word, raw_keyword))

        page_index = re.search(r'(?<=page-)\d+(?=.txt)',
                               key).group(0)

        page_set.append({"page_index": page_index,
                         "name": key, "arr_key": raw_keyword})
        print('end =>', key)

    with cf.ThreadPoolExecutor(max_workers=3) as executor:
        for key, value in documents.items():
            executor.submit(main, key, value)

    # for key, value in documents.items():
    #     main(key, value)

    for page in page_set:
        raw_keyword = page['arr_key']
        ''' stemming term '''
        raw_keyword = list(map(stemming.lemmatizer, raw_keyword))
        sdb.manage_pre_keyword(page, doc_id, raw_keyword)


def calculateTf(listWord):
    unique = create_unique.unique(listWord)
    documentsFreq = create_frame.createFrame(listWord, unique)
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
