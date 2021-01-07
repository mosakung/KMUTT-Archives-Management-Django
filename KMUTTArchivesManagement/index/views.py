from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

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
            documentPK = documentHelper.add()
            pathToDirectory = documentHelper.getPathDicrectory()
            filename = documentHelper.getFileName()
            startPage = documentHelper.getStartPageOCR()

            ocr(filename, pathToDirectory, startPage)

            perTerm = PerTermController(filename, documentPK)
            perTerm.manage()
            documentHelper.done(documentPK)
            print("<END PROCESS> Add Document (", documentPK, ")")
            return True

        permission, message = document.ask()

        if permission:
            main(document)
            # settings.SLOW_POOL.submit(main, document)

        return JsonResponse({
            'status': permission,
            'message': message,
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
            tfidfHelper.done()
            print("<END PROCESS> init TF-IDF Document (", documentIndex, ")")
            return True

        if statusDocument == 1:
            # main(pkDocument)
            settings.FAST_POOL.submit(main, pkDocument)
        else:
            return JsonResponse({
                'message': False,
            })

        return JsonResponse({
            'message': True,
        })


@api_view(['POST'])
def API_Deepcut(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        fulltext = data.get('fulltext')

        tokens = deepcut(fulltext)

        return JsonResponse({
            'tokens': tokens,
        })
