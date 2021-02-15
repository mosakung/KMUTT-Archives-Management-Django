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
            tfidfHelper.done(4)
            tfidfHelper.manage()
            tfidfHelper.done(5)
            print("<END PROCESS> init TF-IDF Document (", documentIndex, ")")
            return True

        if statusDocument == 3:
            # main(pkDocument)
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
        tokens = deepcut(fulltext)

        return JsonResponse({
            'tokens': tokens,
        })
