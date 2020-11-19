import sys
import os
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from threading import Thread
import concurrent.futures as cf
import tensorflow as tf

# service system
from service_nlp import service_sys as ss
# service db
from service_nlp import service_db as sdb
# db
from service_nlp import manage_db as db

from service_nlp.Request.request import send_ping

# GLOBAL parameter
GLOBAL_POOL = cf.ThreadPoolExecutor(max_workers=1)

# Create your views here.


@csrf_exempt
def request_test(request):
    x = send_ping()
    print('x', x.headers)
    print('x2', x.status_code)
    print('x2', x.url)

    return JsonResponse({
        'result': 'hello'
    })


@csrf_exempt
def request_add_document(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        ask_status, ask_message = sdb.askCreateDocument(data['document'])

        def main(input_data):
            print("START : ", request)
            documentJSON = input_data['document']
            try:
                document_detail = sdb.addDocumnet(documentJSON)
            except:
                print("Unexpected error:", sys.exc_info()[0])
            tf = ss.initTF(documentJSON['path'])
            try:
                index_document = document_detail.get(
                    'result_row_document'
                ).get(
                    'document_id'
                )
                new_term = sdb.what_new_term(tf)
                result_update_TF, dict_log_frequency= sdb.updateTermTF(
                    tf, index_document)
                sdb.update_term_idf_score(new_term)
                sdb.update_document_tfidf_score(index_document)
                error_log = ss.error_validate_frequency(dict_log_frequency)
                if error_log:
                    result = sdb.insert_django_log(error_log, index_document, 404)
                else:
                    sdb.insert_django_log(None, index_document, 200)

                print('error_log :', error_log)
            except:
                print("Unexpected error:", sys.exc_info()[0])

        ''' Thread run '''
        if ask_status:
            GLOBAL_POOL.submit(main, data)

        ''' Basic run '''
        # if ask_status:
        #     main(data)

        return JsonResponse({
            'status': ask_status,
            'message': ask_message,
            'prev_body': data
        })
    else:
        return JsonResponse({'request recommend': 'POST request'})


@csrf_exempt
def request_update_IDF(request):
    if request.method == 'GET':

        def main():
            db.update_IDF_all()
            print("update_IDF_all -> DONE")

        GLOBAL_POOL.submit(main)

        return JsonResponse({
            'message': "update all IDF score, wait process"
        })
    else:
        return JsonResponse({'request recommend': 'GET request'})


@csrf_exempt
def request_update_TF_IDF(request):
    if request.method == 'GET':

        def main():
            db.update_score_TFIDF_all()
            db.update_score_TFIDF_all_user()
            print("update_score_TFIDF_all -> DONE")

        GLOBAL_POOL.submit(main)

        return JsonResponse({
            'message': "update all TF-IDF score, wait process"
        })
    else:
        return JsonResponse({'request recommend': 'GET request'})
