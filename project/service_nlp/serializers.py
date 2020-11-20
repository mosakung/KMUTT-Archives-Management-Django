
from rest_framework import serializers
from service_nlp.models import Dc_keyword
from service_nlp.models import Dc_relation
from service_nlp.models import Dc_type
from service_nlp.models import Document
from service_nlp.models import Indexing_contributor_document
from service_nlp.models import Indexing_creator_document
from service_nlp.models import Indexing_creator_orgname_document
from service_nlp.models import Indexing_publisher_document
from service_nlp.models import Indexing_issued_date_document
from service_nlp.models import Score
from service_nlp.models import Term_word
from service_nlp.models import Django_log
from service_nlp.models import Page_in_document
from service_nlp.models import Pre_term_in_page
from service_nlp.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

# dc_keyword serializers


class Dc_keywordSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Dc_keyword
        fields = ('DC_keyword_id',
                  'DC_keyword',
                  'index_document_id')

# dc_relation serializers


class Dc_relationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Dc_relation
        fields = ('DC_relation_id',
                  'DC_relation',
                  'index_document_id')

# dc_type serializers


class Dc_typeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Dc_type
        fields = ('DC_type_id',
                  'DC_type',
                  'index_document_id')


# document serializers


class DocumentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Document
        fields = ('document_id',
                  'status_process_document',
                  'name',
                  'version',
                  'path',
                  'DC_title',
                  'DC_title_alternative',
                  'DC_description_table_of_contents',
                  'DC_description_summary_or_abstract',
                  'DC_description_note',
                  'DC_format',
                  'DC_format_extent',
                  'DC_identifier_URL',
                  'DC_identifier_ISBN',
                  'DC_source',
                  'DC_language',
                  'DC_coverage_spatial',
                  'DC_coverage_temporal',
                  'DC_rights',
                  'DC_rights_access',
                  'thesis_degree_name',
                  'thesis_degree_level',
                  'thesis_degree_discipline',
                  'thesis_degree_grantor',
                  'rec_create_at',
                  'rec_create_by',
                  'rec_modified_at',
                  'rec_modified_by',
                  'index_creator',
                  'index_creator_orgname',
                  'index_publisher',
                  'index_contributor',)

# indexing_contributor_document serializers


class Indexing_contributor_documentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_contributor_document
        fields = ('indexing_contributor_id',
                  'contributor',
                  'contributor_role',
                  'frequency',)
# indexing_creator_document serializers


class Indexing_creator_documentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_creator_document
        fields = ('indexing_creator_id',
                  'creator',
                  'frequency')
# indexing_creator_orgname_document serializers


class Indexing_creator_orgname_documentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_creator_orgname_document
        fields = ('indexing_creator_orgname_id',
                  'creator_orgname',
                  'frequency')

# indexing_publisher_document serializers


class Indexing_publisher_documentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_publisher_document
        fields = ('indexing_publisher_id',
                  'publisher',
                  'publisher_email',
                  'frequency')

# indexing_issued_date_document serializers


class Indexing_issued_date_documentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_issued_date_document
        fields = ('indexing_issued_date_id',
                  'issued_date',
                  'frequency',)

# score serializers


class ScoreSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Score
        fields = ('score_id',
                  'score_tf',
                  'score_tf_idf',
                  'index_term_word_id',
                  'index_document_id',
                  'generate_by',
                  'rec_status')

# term_word_id serializers


class Term_wordSerializer(DynamicFieldsModelSerializer):
    score_idf = serializers.CharField(max_length=191)

    class Meta:
        model = Term_word
        fields = ('term_word_id',
                  'term',
                  'frequency',
                  'score_idf',
                  'rec_create_at',
                  'rec_modified_at')


class Django_logSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Django_log
        fields = ('django_log_id',
                  'rec_status',
                  'rec_create_date',
                  'log_error',
                  'index_document')


class Page_in_documentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Page_in_document
        fields = ('page_in_document_id',
                  'page_index',
                  'name',
                  'rec_status_confirm',
                  'index_document_id')


class Pre_term_in_pageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Pre_term_in_page
        fields = ('pre_term_in_page_id',
                  'pre_term',
                  'index_page_in_document_id')


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('user_id',
                  'name',
                  'surname',
                  'role',
                  'username',
                  'password',
                  'create_at',
                  'active')
