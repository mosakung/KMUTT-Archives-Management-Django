from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import tensorflow as tf

from modelUser.views import UserController
from modelDocument.views import DocumentController
from modelDocument.views import getDocumentStatus
from modelDocument.views import updateStatus
from modelPreTerm.views import PerTermController
from modelPreTerm.views import PerTermRepository
from modelTerm.views import TfIdf
from ocr.tesseract import main as ocr
from django.conf import settings

from tokenizer.deepcut import deepcut


@api_view(['POST'])
def API_Add_Document(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        document = DocumentController(data)

        def main(documentHelper):
            documentPK = documentHelper.getDocumentId()
            pathToDirectory = documentHelper.getPathDicrectory()
            filename = documentHelper.getFileName()
            startPage = documentHelper.getStartPageOCR()
            documentHelper.done(documentPK, 1)
            ocr(filename, pathToDirectory, startPage)
            documentHelper.done(documentPK, 2)
            documentHelper.updateAmountPage()
            perTerm = PerTermController(filename, documentPK)
            perTerm.manage()
            documentHelper.done(documentPK, 3)
            print("<END PROCESS> Add Document (", documentPK, ")")
            return True

        permission, message = document.ask()

        if permission:
            documentId = document.add()
            # main(document)
            settings.SLOW_POOL.submit(main, document)
        else:
            documentId = None

        return JsonResponse({
            'status': permission,
            'message': message,
            'documentId': documentId,
            'prev_body': data,
        })


@api_view(['POST'])
def API_INIT_TF(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        pkDocument = data.get('documentId')

        if pkDocument == None:
            return JsonResponse({
                'message': False,
            })

        statusDocument = getDocumentStatus(pkDocument)

        def main(documentIndex):
            repo = PerTermRepository(documentIndex)
            terms = repo.query()
            tfidfHelper = TfIdf(terms, documentIndex)
            tfidfHelper.manage()
            tfidfHelper.done(5)
            print("<END PROCESS> init TF-IDF Document (", documentIndex, ")")
            return True

        if statusDocument == 3:
            # main(pkDocument)
            updateStatus(pkDocument, 4)
            settings.FAST_POOL.submit(main, pkDocument)
        else:
            return JsonResponse({
                'status': False,
                'message': 'The documenting process does not match this procedure',
            })

        return JsonResponse({
            'status': True,
            'message': 'TFIDF initialization is in progress, please wait',
        })


@api_view(['POST'])
def API_Deepcut(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        fulltext = data.get('fulltext')
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

        tokens = []
        for text in fulltext.split(" "):
            rawTokens = deepcut(text)
            tokens.extend(rawTokens)

        tokensClean = list(filter(
            lambda token: token != ' ' and token != '', tokens
        ))

        uniqueTokens = []
        for token in tokensClean:
            if not (token in uniqueTokens):
                uniqueTokens.append(token)

        similarTokens = []
        for token in uniqueTokens:
            try:
                similar = settings.MODEL_WORD2VEC.wv.similar_by_word(token)
                resultSimilar = []
                for sml in similar:
                    resultSimilar.append({
                        'token': sml[0],
                        'score': sml[1]
                    })
                similarTokens.append({
                    'key': token,
                    'value': resultSimilar
                })
            except KeyError:
                similarTokens.append({
                    'key': token,
                    'value': []
                })

        print({
            'tokens': uniqueTokens,
            'similarTokens': similarTokens,
        })

        return JsonResponse({
            'tokens': uniqueTokens,
            'similarTokens': similarTokens,
        })
