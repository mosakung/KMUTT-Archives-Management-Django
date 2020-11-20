from service_nlp import manage_db as db


def askCreateDocument(body, add_version=False):
    if body.get('name') == None:
        return False, "pls input name document"
    status_already_document, version = db.alreadyDocumnet(body['name'])
    if "add_version" in body:
        if body["add_version"] == True:
            add_version = True
    if(status_already_document and not add_version):
        return False, "already document name pls change name or set add_version=True"
    return True, "can add document wait process"


def addDocumnet(body):
    result_dict = {}
    status_already_document, rec_version = db.alreadyDocumnet(body['name'])
    body.update({"version": rec_version + 1})

    if not body.get('DC_contributor') == None:
        result_row_contributor = db.updateFrequency_Indexing_contributor_document(
            body
        )
        index_contributor = result_row_contributor['indexing_contributor_id']
        body.update({"index_contributor": index_contributor})
        result_dict.update({'result_row_contributor': result_row_contributor})

    if not body.get('DC_creator') == None:
        result_row_creator = db.updateFrequency_Indexing_creator_document(
            body
        )
        index_creator = result_row_creator['indexing_creator_id']
        body.update({"index_creator": index_creator})
        result_dict.update({"result_row_creator": result_row_creator})

    if not body.get('DC_creator_orgname') == None:
        result_row_creator_orgname = db.updateFrequency_Indexing_creator_orgname_document(
            body
        )
        index_creator_orgname = result_row_creator_orgname['indexing_creator_orgname_id']
        body.update({"index_creator_orgname": index_creator_orgname})
        result_dict.update(
            {"result_row_creator_orgname": result_row_creator_orgname})

    if not body.get('DC_publisher') == None:
        result_row_publisher = db.updateFrequency_Indexing_publisher_document(
            body
        )
        index_publisher = result_row_publisher['indexing_publisher_id']
        body.update({"index_publisher": index_publisher})
        result_dict.update({"result_row_publisher": result_row_publisher})

    if not body.get('DC_issued_date') == None:
        result_row_issued_date = db.updateFrequency_Indexing_issued_date_document(
            body
        )
        indexing_issued_date = result_row_issued_date['indexing_issued_date_id']
        body.update({"indexing_issued_date": indexing_issued_date})
        result_dict.update(
            {"result_row_issued_date": result_row_issued_date})

    result_row_document = db.insertDocument(body)
    index_documnet = result_row_document['document_id']
    result_dict.update({"result_row_document": result_row_document})

    # if not body.get('DC_keyword') == None:
    #     arr_dc_keyword = body['DC_keyword']
    #     result_row_keyword_all = []
    #     for value in arr_dc_keyword:
    #         param = {
    #             "DC_keyword": value,
    #             "index_document_id": index_documnet
    #         }
    #         result_row_keyword = db.insertDC_keyword(param)
    #         result_row_keyword_all.append(result_row_keyword)
    #     result_dict.update({"result_row_keyword": result_row_keyword_all})

    if not body.get('DC_relation') == None:
        arr_dc_relation = body['DC_relation']
        result_row_relation_all = []
        for value in arr_dc_relation:
            param = {
                "DC_relation": value,
                "index_document_id": index_documnet
            }
            result_row_relation = db.insertDC_relation(param)
            result_row_relation_all.append(result_row_relation)
        result_dict.update({"result_row_relation": result_row_relation_all})

    if not body.get('DC_type') == None:
        arr_dc_type = body['DC_type']
        result_row_type_all = []
        for value in arr_dc_type:
            param = {
                "DC_type": value,
                "index_document_id": index_documnet
            }
            result_row_type = db.insertDC_type(param)
            result_row_type_all.append(result_row_type)
        result_dict.update({"result_row_relation": result_row_type_all})

    return result_dict


def updateTermTF(tf_set, index_document):
    result_term = []
    dict_log_frequency = {}
    for key, value in tf_set.items():
        result_row_term = db.updateFrequency_Term_word(key)
        key_term_from_db = result_row_term['term']
        # if(key != key_term_from_db):
        #     print("NOT EQUAL : (RAW) ", key, " | (DB)", key_term_from_db)
        if dict_log_frequency.get(key_term_from_db) == None:
            dict_log_frequency.update({key_term_from_db: 1})
        else:
            dict_log_frequency[key_term_from_db] += 1
        index_term = result_row_term.get('term_word_id')
        db.insertScore(index_term, index_document, value)
        result_term.append(result_term)

    return result_term, dict_log_frequency


def what_new_term(tf_set):
    tf_key = tf_set.keys()
    rows = db.select_if_have(tf_key)
    new_key = list(set(tf_key) - set(rows))
    return new_key


def update_term_idf_score(set_term_update):
    N = db.count_N_document()
    res_all = []
    for term in set_term_update:
        res = db.update_IDF_mono(term, N)
        res_all.append(res)
    return res_all


def update_document_tfidf_score(index_document):
    res_system = db.update_score_TFIDF_mono(index_document)
    return res_system


def insert_django_log(log, index_document, status):
    logDetails = {
        "status": status,
        "log_error": log,
        "index_document": index_document
    }
    row = db.insert_error_create_doc(logDetails)
    return row


def manage_pre_keyword(page_body, document_id, keywords):
    name = page_body['name']
    index = page_body['page_index']

    row_page = db.insert_page(index, name, document_id)
    page_id = row_page.get('page_in_document_id')

    for keyword in keywords:
        row_pre_term = db.insert_pre_term_in_page(keyword, page_id)


def task_initialize_PRE_keyword_done(document_id):
    return db.update_status_document(document_id, 1)


def task_initialize_TF_IDF_done(document_id):
    return db.update_status_document(document_id, 2)


def query_term_for_TF(document_id):
    arrayPages = db.query_page_in_document_id(document_id)
    arrayTerms = list(map(lambda x: db.query_term_in_page(
        x['page_in_document_id']), arrayPages))
    result = []
    for arrayTerm in arrayTerms:
        array = list(map(lambda x: x['pre_term'], arrayTerm))
        result.extend(array)
    return result
