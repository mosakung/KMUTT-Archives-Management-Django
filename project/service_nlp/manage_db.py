import math
from django.db.models import Max, F, OuterRef, Subquery, Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.dateparse import parse_date
# Dc_keyword
from service_nlp.models import Dc_keyword
from service_nlp.serializers import Dc_keywordSerializer
# Dc_relation
from service_nlp.models import Dc_relation
from service_nlp.serializers import Dc_relationSerializer
# Dc_type
from service_nlp.models import Dc_type
from service_nlp.serializers import Dc_typeSerializer
# Document
from service_nlp.models import Document
from service_nlp.serializers import DocumentSerializer
# Indexing_contributor_document
from service_nlp.models import Indexing_contributor_document
from service_nlp.serializers import Indexing_contributor_documentSerializer
# Indexing_creator_document
from service_nlp.models import Indexing_creator_document
from service_nlp.serializers import Indexing_creator_documentSerializer
# Indexing_creator_orgname_document
from service_nlp.models import Indexing_creator_orgname_document
from service_nlp.serializers import Indexing_creator_orgname_documentSerializer
# Indexing_publisher_document
from service_nlp.models import Indexing_publisher_document
from service_nlp.serializers import Indexing_publisher_documentSerializer
# Indexing_issued_date_document
from service_nlp.models import Indexing_issued_date_document
from service_nlp.serializers import Indexing_issued_date_documentSerializer
# Score
from service_nlp.models import Score
from service_nlp.serializers import ScoreSerializer
# Term_word
from service_nlp.models import Term_word
from service_nlp.serializers import Term_wordSerializer
# django_log
from service_nlp.models import Django_log
from service_nlp.serializers import Django_logSerializer
# Page_in_document
from service_nlp.models import Page_in_document
from service_nlp.serializers import Page_in_documentSerializer
# Pre_term_in_page
from service_nlp.models import Pre_term_in_page
from service_nlp.serializers import Pre_term_in_pageSerializer


def insertIndexing_contributor_document(body):
    if body.get('DC_contributor') == None:
        return False
    row = Indexing_contributor_document(
        contributor=body.get('DC_contributor'),
        contributor_role=body.get('DC_contributor_role'),
        frequency=1
    )
    row.save()
    serializers = Indexing_contributor_documentSerializer(row)
    result = serializers.data

    return result


def updateFrequency_Indexing_contributor_document(body):
    if body.get('DC_contributor') == None:
        return False
    try:
        row = Indexing_contributor_document.objects.get(
            contributor=body['DC_contributor']
        )
        row.frequency += 1
        row.save()
        serializers = Indexing_contributor_documentSerializer(row)
        result = serializers.data
        return result
    except Indexing_contributor_document.DoesNotExist:
        return insertIndexing_contributor_document(body)
    except Indexing_contributor_document.MultipleObjectsReturned:
        return False

# Indexing_creator_document


def insertIndexing_creator_document(body):
    row = Indexing_creator_document(
        creator=body.get('DC_creator'),
        frequency=1
    )
    row.save()
    serializers = Indexing_creator_documentSerializer(row)
    result = serializers.data

    return result


def updateFrequency_Indexing_creator_document(body):
    if body.get('DC_creator') == None:
        return False
    try:
        row = Indexing_creator_document.objects.get(
            creator=body['DC_creator']
        )
        row.frequency += 1
        row.save()
        serializers = Indexing_creator_documentSerializer(row)
        result = serializers.data
        return result
    except Indexing_creator_document.DoesNotExist:
        return insertIndexing_creator_document(body)
    except Indexing_creator_document.MultipleObjectsReturned:
        return False

# Indexing_creator_orgname_document


def insertIndexing_creator_orgname_document(body):
    row = Indexing_creator_orgname_document(
        creator_orgname=body.get('DC_creator_orgname'),
        frequency=1
    )
    row.save()
    serializers = Indexing_creator_orgname_documentSerializer(row)
    result = serializers.data

    return result


def updateFrequency_Indexing_creator_orgname_document(body):
    if body.get('DC_creator_orgname') == None:
        return False
    try:
        row = Indexing_creator_orgname_document.objects.get(
            creator_orgname=body['DC_creator_orgname']
        )
        row.frequency += 1
        row.save()
        serializers = Indexing_creator_orgname_documentSerializer(row)
        result = serializers.data
        return result
    except Indexing_creator_orgname_document.DoesNotExist:
        return insertIndexing_creator_orgname_document(body)
    except Indexing_creator_orgname_document.MultipleObjectsReturned:
        return False


# Indexing_publisher_document


def insertIndexing_publisher_document(body):
    row = Indexing_publisher_document(
        publisher=body.get('DC_publisher'),
        publisher_email=body.get('DC_publisher_email'),
        frequency=1
    )
    row.save()
    serializers = Indexing_publisher_documentSerializer(row)
    result = serializers.data

    return result


def updateFrequency_Indexing_publisher_document(body):
    if body.get('DC_publisher') == None:
        return False
    try:
        row = Indexing_publisher_document.objects.get(
            publisher=body['DC_publisher']
        )
        row.frequency += 1
        row.save()
        serializers = Indexing_publisher_documentSerializer(row)
        result = serializers.data
        return result
    except Indexing_publisher_document.DoesNotExist:
        return insertIndexing_publisher_document(body)
    except Indexing_publisher_document.MultipleObjectsReturned:
        return False

# Indexing_issued_date_document


def insertIndexing_issued_date_document(body):
    row = Indexing_issued_date_document(
        issued_date=parse_date(body['DC_issued_date']),
        frequency=1
    )
    row.save()
    serializers = Indexing_issued_date_documentSerializer(row)
    result = serializers.data

    return result


def updateFrequency_Indexing_issued_date_document(body):
    if body.get('DC_issued_date') == None:
        return False
    try:
        row = Indexing_issued_date_document.objects.get(
            issued_date=parse_date(body['DC_issued_date'])
        )
        row.frequency += 1
        row.save()
        serializers = Indexing_issued_date_documentSerializer(row)
        result = serializers.data
        return result
    except Indexing_issued_date_document.DoesNotExist:
        return insertIndexing_issued_date_document(body)
    except Indexing_issued_date_document.MultipleObjectsReturned:
        return False

# Documnet


def alreadyDocumnet(name):
    try:
        documents = Document.objects.filter(name=name)
        current_version = documents.aggregate(Max('version'))
        if not documents:
            return False, 0
        rec_version = current_version['version__max']
        return True, rec_version
    except:
        print("\n== file[manage_db.py] def[alreadyDocumnet] except ==\n")


def insertDocument(body):
    row = Document(
        status_process_document=0,
        name=body.get('name'),
        version=body.get('version'),
        path=body.get('path'),
        DC_title=body.get('DC_title'),
        DC_title_alternative=body.get('DC_title_alternative'),
        DC_description_table_of_contents=body.get(
            'DC_description_table_of_contents'
        ),
        DC_description_summary_or_abstract=body.get(
            'DC_description_summary_or_abstract'
        ),
        DC_description_note=body.get('DC_description_note'),
        DC_format=body.get('DC_format'),
        DC_format_extent=body.get('DC_format_extent'),
        DC_identifier_URL=body.get('DC_identifier_URL'),
        DC_identifier_ISBN=body.get('DC_identifier_ISBN'),
        DC_source=body.get('DC_source'),
        DC_language=body.get('DC_language'),
        DC_coverage_spatial=body.get('DC_coverage_spatial'),
        DC_coverage_temporal=body.get('DC_coverage_temporal'),
        DC_rights=body.get('DC_rights'),
        DC_rights_access=body.get('DC_rights_access'),
        thesis_degree_name=body.get('thesis_degree_name'),
        thesis_degree_level=body.get('thesis_degree_level'),
        thesis_degree_discipline=body.get('thesis_degree_discipline'),
        thesis_degree_grantor=body.get('thesis_degree_grantor'),
        index_creator=body.get('index_creator'),
        index_creator_orgname=body.get('index_creator_orgname'),
        index_publisher=body.get('index_publisher'),
        index_contributor=body.get('index_contributor'),
        index_issued_date=body.get('indexing_issued_date'),
        rec_create_by=body.get('rec_create_by'),
        rec_modified_by=body.get('rec_create_by')
    )
    row.save()
    serializers = DocumentSerializer(row)
    result = serializers.data

    return result


def count_N_document():
    len_documents = Document.objects.count()
    return len_documents

# DC_keyword


def insertDC_keyword(body):
    row = Dc_keyword(
        DC_keyword=body.get('DC_keyword'),
        index_document_id=body.get('index_document_id')
    )
    row.save()
    serializers = Dc_keywordSerializer(row)
    result = serializers.data
    return result

# DC_relation


def insertDC_relation(body):
    row = Dc_relation(
        DC_relation=body.get('DC_relation'),
        index_document_id=body.get('index_document_id')
    )
    row.save()
    serializers = Dc_relationSerializer(row)
    result = serializers.data
    return result

# DC_type


def insertDC_type(body):
    row = Dc_type(
        DC_type=body.get('DC_type'),
        index_document_id=body.get('index_document_id'))
    row.save()
    serializers = Dc_typeSerializer(row)
    result = serializers.data
    return result

# Term_word


def select_if_have(term_set):
    row = Term_word.objects.filter(
        term__in=term_set
    ).values_list('term', flat=True).distinct()

    return row


def getUniqueTerm():
    fields = ('term_word_id', 'term')
    term_words = Term_word.objects.all()
    serializers = Term_wordSerializer(term_words, many=True, fields=fields)
    result = serializers.data
    return result


def select_term_word(term):
    try:
        row = Term_word.objects.get(
            term=term
        )
        serializers = Term_wordSerializer(row)
        result = serializers.data
        return result
    except Term_word.DoesNotExist:
        return insertTerm_word(term)
    except Term_word.MultipleObjectsReturned:
        return False


def insertTerm_word(term):
    row = Term_word(
        term=term,
        frequency=1,
    )
    row.save()
    serializers = Term_wordSerializer(row)
    result = serializers.data
    return result


def updateFrequency_Term_word(term):
    try:
        row = Term_word.objects.get(
            term=term
        )
        row.frequency += 1
        row.save()
        serializers = Term_wordSerializer(row)
        result = serializers.data
        return result
    except Term_word.DoesNotExist:
        return insertTerm_word(term)
    except Term_word.MultipleObjectsReturned:
        return False


def update_IDF_mono(term, N):
    try:
        row = Term_word.objects.get(
            term=term
        )
        row.score_idf = math.log10(N / row.frequency)
        row.save()
        serializers = Term_wordSerializer(row)

        # return result
    except Term_word.DoesNotExist:
        return False
    except Term_word.MultipleObjectsReturned:
        return False


def update_IDF_all(N):
    rows = Term_word.objects.all()
    rows.update(score_idf=math.log10(N / F('frequency')))
    serializers = Term_wordSerializer(rows, many=True)
    result = serializers.data
    return result

# score


def insertScore(term_index, doc_index, score):
    row = Score(
        score_tf=score,
        index_term_word_id=term_index,
        index_document_id=doc_index,
        score_tf_idf=None
    )
    row.save()
    serializers = ScoreSerializer(row)
    result = serializers.data
    return result


def update_score_TFIDF_mono(doc_index):
    rows = Score.objects.filter(
        ~Q(generate_by="init-user"),
        index_document_id=doc_index
    )
    rows.update(
        score_tf_idf=F('score_tf') * Subquery(
            Term_word.objects.filter(
                term_word_id=OuterRef('index_term_word_id')
            ).values('score_idf')
        ),
        generate_by="init_system"
    )
    serializers = ScoreSerializer(rows, many=True)
    result = serializers.data
    return result


def update_score_TFIDF_all():
    rows = Score.objects.filter(
        ~Q(generate_by="init-user")
    )
    rows.update(
        score_tf_idf=F('score_tf') * Subquery(
            Term_word.objects.filter(
                term_word_id=OuterRef('index_term_word_id')
            ).values('score_idf')
        ),
        generate_by="init_system"
    )
    serializers = ScoreSerializer(rows, many=True)
    result = serializers.data
    return result


def update_score_TFIDF_all_user():
    all_row = Score.objects.all()
    max_list = all_row.aggregate(Max('score_tf_idf'))
    max_score_tf_idf = max_list['score_tf_idf__max']
    rows = Score.objects.filter(
        generate_by="init-user"
    )
    rows.update(
        score_tf_idf=max_score_tf_idf
    )
    serializers = ScoreSerializer(rows, many=True)
    result = serializers.data
    return result

# view


def query_by_term(term_word_input):
    rows = Term_word.objects.filter(
        term=term_word_input
    )


''' add score TF-IDF by user table '''


def insert_score_tag_user(term_index, doc_index):
    row = Score(
        score_tf=-1,
        index_term_word_id=term_index,
        index_document_id=doc_index,
        score_tf_idf=-1,
        generate_by="init-user"
    )
    row.save()
    serializers = ScoreSerializer(row)
    result = serializers.data
    return result


def update_score_tag_user(term_index, doc_index):
    try:
        row = Score.objects.get(
            index_term_word_id=term_index,
            index_document_id=doc_index
        )
        row.generate_by = "init-user"
        row.score_tf_idf = -1
        row.save()
        serializers = ScoreSerializer(row)
        result = serializers.data
        return result
    except Score.DoesNotExist:
        return insert_score_tag_user(term_index, doc_index)
    except Score.MultipleObjectsReturned:
        return False


def insert_error_create_doc(logDetails):
    row = Django_log(
        rec_status=logDetails['status'],
        log_error=logDetails['log_error'],
        index_document=logDetails['index_document']
    )
    row.save()
    serializers = Django_logSerializer(row)
    result = serializers.data
    return result


def insert_page(index, name, document_id):
    row = Page_in_document(
        page_index=index,
        name=name,
        index_document_id=document_id,
        rec_status_confirm=0
    )
    row.save()
    serializers = Page_in_documentSerializer(row)
    result = serializers.data
    return result


def insert_pre_term_in_page(term, page_id):
    row = Pre_term_in_page(
        pre_term=term,
        index_page_in_document_id=page_id
    )
    row.save()
    serializers = Pre_term_in_pageSerializer(row)
    result = serializers.data
    return result


def update_status_document(document_id, status):
    try:
        row = Document.objects.get(
            document_id=document_id,
        )
        row.status_process_document = status
        row.save()
        serializers = DocumentSerializer(row)
        result = serializers.data
        return result
    except Document.DoesNotExist:
        return False
    except Document.MultipleObjectsReturned:
        return False


def query_page_in_document_id(document_id):
    rows = Page_in_document.objects.filter(
        index_document_id=document_id
    )
    serializers = Page_in_documentSerializer(rows, many=True)
    result = serializers.data
    return result


def query_term_in_page(page_docId):
    rows = Pre_term_in_page.objects.filter(
        index_page_in_document_id=page_docId
    )
    serializers = Pre_term_in_pageSerializer(rows, many=True)
    result = serializers.data
    return result
