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
from django.shortcuts import render
from django.db.models import Max, F, OuterRef, Subquery, Q
from tokenizer.pipeLineToken import pipeLineTokenizer
import tensorflow as tf

from modelPreTerm.models import *
from modelPreTerm.serializers import *


class PageInDocumentController():
    def __init__(self, index_document, **kwargs):
        super().__init__(**kwargs)
        self.index_document = index_document

    def queryPage(self):
        page = Page_in_document.objects.filter(
            index_document_id=self.index_document
        )
        serializer = PageInDocumentSerializer(page, many=True)
        return serializer.data

    def insertPage(self, filename, pageIndex):
        insertData = {
            "page_index": pageIndex,
            "name": filename,
            "rec_status_confirm": 0,
            "index_document_id": self.index_document
        }
        serializer = PageInDocumentSerializer(data=insertData)
        if serializer.is_valid():
            serializer.save()
            result = serializer.data
            return result.get('page_in_document_id')
        print(serializer.errors)
        return False


class PerTermInPageController():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def queryPerTermInPage(self, pageIndexKey):
        perterms = Pre_term_in_page.objects.filter(
            index_page_in_document_id=pageIndexKey
        )
        serializer = PreTermInPageSerializer(perterms, many=True)
        return serializer.data

    def insertKeywords(self, keywords, pageIndex):
        result = []
        for keyword in keywords:
            insertData = {
                "pre_term": keyword,
                "index_page_in_document_id": pageIndex
            }
            serializer = PreTermInPageSerializer(data=insertData)
            if serializer.is_valid():
                serializer.save()
                result.append(serializer.data)
            else:
                print(serializer.errors)
                result.append(False)
        return result


class PerTermController(PageInDocumentController, PerTermInPageController):

    def __init__(self, directoryName, index_document):
        self.directoryName = '/' + directoryName
        self.index_document = index_document
        self.pathToDirectory = './document-report/' + directoryName
        super().__init__(
            index_document=self.index_document
        )

    def manage(self, verbose=True):
        pageSet = []
        directory = readDirectory(self.pathToDirectory)
        pool = Pool(processes=3)
        GLOBAL_POSITION_PROCESS_BAR = {"0": False, "1": False, "2": False}

        for filename, fulltext in directory.items():
            pool.apply_async(pipeLineTokenizer, args=(filename, fulltext, ),
                             callback=pageSet.append)

        pool.close()
        pool.join()

        # for filename, fulltext in directory.items():
        #     main(filename, fulltext)
        for page in pageSet:
            keys = page.get('rawKeywords')
            filename = page.get('filename')
            pageIndex = page.get('pageIndex')

            # Lemmatizer
            keys = list(map(lemmatizer, keys))
            pkPage = self.insertPage(filename, pageIndex)
            self.insertKeywords(keys, pkPage)


class PerTermRepository(PageInDocumentController, PerTermInPageController):

    def __init__(self, pkDocument):
        self.pkDocument = pkDocument

        super().__init__(
            index_document=self.pkDocument
        )

    def query(self):
        result = []
        pages = self.queryPage()
        terms_arr = list(map(lambda page: self.queryPerTermInPage(
            page.get('page_in_document_id')),
            pages))

        for terms in terms_arr:
            term = list(map(lambda x: x.get('pre_term'), terms))
            result.extend(term)

        result = list(filter(filterStopword, result))

        return result
