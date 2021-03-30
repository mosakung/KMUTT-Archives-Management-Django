from rest_framework import serializers
from modelDocument.models import *


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


class DocumentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Document
        fields = ('document_id',
                  'status_process_document',
                  'name',
                  'version',
                  'page_start',
                  'amount_page',
                  'path',
                  'path_image',
                  'DC_title',
                  'DC_title_alternative',
                  'DC_description_table_of_contents',
                  'DC_description_summary',
                  'DC_description_abstract',
                  'DC_description_note',
                  'DC_format',
                  'DC_format_extent',
                  'DC_identifier_URL',
                  'DC_identifier_ISBN',
                  'DC_source',
                  'DC_language',
                  'DC_coverage_spatial',
                  'DC_coverage_temporal',
                  'DC_coverage_temporal_year',
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
                  'index_issued_date',
                  'index_publisher_email',
                  'rec_status')

    def create(self, validated_data):
        return Document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.document_id = validated_data.get(
            'document_id', instance.document_id)
        instance.status_process_document = validated_data.get(
            'status_process_document', instance.status_process_document)
        instance.name = validated_data.get('name', instance.name)
        instance.version = validated_data.get('version', instance.version)
        instance.page_start = validated_data.get(
            'page_start', instance.page_start)
        instance.amount_page = validated_data.get(
            'amount_page', instance.amount_page)
        instance.path = validated_data.get('path', instance.path)
        instance.path_image = validated_data.get(
            'path_image', instance.path_image)
        instance.DC_title = validated_data.get('DC_title', instance.DC_title)
        instance.DC_title_alternative = validated_data.get(
            'DC_title_alternative', instance.DC_title_alternative)
        instance.DC_description_table_of_contents = validated_data.get(
            'DC_description_table_of_contents', instance.DC_description_table_of_contents)
        instance.DC_description_summary = validated_data.get(
            'DC_description_summary', instance.DC_description_summary)
        instance.DC_description_abstract = validated_data.get(
            'DC_description_abstract', instance.DC_description_abstract)
        instance.DC_description_note = validated_data.get(
            'DC_description_note', instance.DC_description_note)
        instance.DC_format = validated_data.get(
            'DC_format', instance.DC_format)
        instance.DC_format_extent = validated_data.get(
            'DC_format_extent', instance.DC_format_extent)
        instance.DC_identifier_URL = validated_data.get(
            'DC_identifier_URL', instance.DC_identifier_URL)
        instance.DC_identifier_ISBN = validated_data.get(
            'DC_identifier_ISBN', instance.DC_identifier_ISBN)
        instance.DC_source = validated_data.get(
            'DC_source', instance.DC_source)
        instance.DC_language = validated_data.get(
            'DC_language', instance.DC_language)
        instance.DC_coverage_spatial = validated_data.get(
            'DC_coverage_spatial', instance.DC_coverage_spatial)
        instance.DC_coverage_temporal = validated_data.get(
            'DC_coverage_temporal', instance.DC_coverage_temporal)
        DC_coverage_temporal_year = validated_data.get(
            'DC_coverage_temporal_year', instance.DC_coverage_temporal_year)
        instance.DC_rights = validated_data.get(
            'DC_rights', instance.DC_rights)
        instance.DC_rights_access = validated_data.get(
            'DC_rights_access', instance.DC_rights_access)
        instance.thesis_degree_name = validated_data.get(
            'thesis_degree_name', instance.thesis_degree_name)
        instance.thesis_degree_level = validated_data.get(
            'thesis_degree_level', instance.thesis_degree_level)
        instance.thesis_degree_discipline = validated_data.get(
            'thesis_degree_discipline', instance.thesis_degree_discipline)
        instance.thesis_degree_grantor = validated_data.get(
            'thesis_degree_grantor', instance.thesis_degree_grantor)
        instance.rec_create_at = validated_data.get(
            'rec_create_at', instance.rec_create_at)
        instance.rec_create_by = validated_data.get(
            'rec_create_by', instance.rec_create_by)
        instance.rec_modified_at = validated_data.get(
            'rec_modified_at', instance.rec_modified_at)
        instance.rec_modified_by = validated_data.get(
            'rec_modified_by', instance.rec_modified_by)
        instance.index_creator = validated_data.get(
            'index_creator', instance.index_creator)
        instance.index_creator_orgname = validated_data.get(
            'index_creator_orgname', instance.index_creator_orgname)
        instance.index_publisher = validated_data.get(
            'index_publisher', instance.index_publisher)
        instance.index_publisher_email = validated_data.get(
            'index_publisher_email', instance.index_publisher_email)
        instance.index_contributor = validated_data.get(
            'rec_status', instance.rec_status)
        instance.save()
        return instance


class DcKeywordSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Dc_keyword
        fields = ('DC_keyword_id',
                  'DC_keyword',
                  'index_document_id')

    def create(self, validated_data):
        return Dc_keyword.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.DC_keyword_id = validated_data.get(
            'DC_keyword_id', instance.DC_keyword_id)
        instance.DC_keyword = validated_data.get(
            'DC_keyword', instance.DC_keyword)
        instance.index_document_id = validated_data.get(
            'index_document_id', instance.index_document_id)
        instance.save()
        return instance


class DcContributorsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Dc_contributors
        fields = ('DC_contributors_id',
                  'index_contributor_id',
                  'index_document_id')

    def create(self, validated_data):
        return Dc_contributors.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.DC_contributors_id = validated_data.get(
            'DC_contributors_id', instance.DC_contributors_id)
        instance.index_contributor_id = validated_data.get(
            'index_contributor_id', instance.index_contributor_id)
        instance.index_document_id = validated_data.get(
            'index_document_id', instance.index_document_id)
        instance.save()
        return instance


class DcRelationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Dc_relation
        fields = ('DC_relation_id',
                  'DC_relation',
                  'index_document_id')

    def create(self, validated_data):
        return Dc_relation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.DC_relation_id = validated_data.get(
            'DC_relation_id', instance.DC_relation_id)
        instance.DC_relation = validated_data.get(
            'DC_relation', instance.DC_relation)
        instance.index_document_id = validated_data.get(
            'index_document_id', instance.index_document_id)
        instance.save()
        return instance


class DcTypeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Dc_type
        fields = ('DC_type_id',
                  'DC_type',
                  'index_document_id')

    def create(self, validated_data):
        return Dc_type.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.DC_type_id = validated_data.get(
            'DC_type_id', instance.DC_type_id)
        instance.DC_type = validated_data.get('DC_type', instance.DC_type)
        instance.index_document_id = validated_data.get(
            'index_document_id', instance.index_document_id)
        instance.save()
        return instance


class IndexingContributorDocumentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_contributor_document
        fields = ('indexing_contributor_id',
                  'contributor',
                  'frequency',)

    def create(self, validated_data):
        return Indexing_contributor_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.indexing_contributor_id = validated_data.get(
            'indexing_contributor_id', instance.indexing_contributor_id)
        instance.contributor = validated_data.get(
            'contributor', instance.contributor)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.save()
        return instance


class IndexingContributorRoleDocumentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Indexing_contributor_role_document
        fields = ('indexing_contributor_role_id',
                  'contributor_role',
                  'index_contributor',)

    def create(self, validated_data):
        return Indexing_contributor_role_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.indexing_contributor_role_id = validated_data.get(
            'indexing_contributor_role_id', instance.indexing_contributor_role_id)
        instance.contributor_role = validated_data.get(
            'contributor_role', instance.contributor_role)
        instance.index_contributor = validated_data.get(
            'index_contributor', instance.index_contributor)
        instance.save()
        return instance


class IndexingCreatorDocumentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_creator_document
        fields = ('indexing_creator_id',
                  'creator',
                  'frequency')

    def create(self, validated_data):
        return Indexing_creator_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.indexing_creator_id = validated_data.get(
            'indexing_creator_id', instance.indexing_creator_id)
        instance.creator = validated_data.get('creator', instance.creator)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.save()
        return instance


class IndexingCreatorOrgnameDocumentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_creator_orgname_document
        fields = ('indexing_creator_orgname_id',
                  'creator_orgname',
                  'frequency')

    def create(self, validated_data):
        return Indexing_creator_orgname_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.indexing_creator_orgname_id = validated_data.get(
            'indexing_creator_orgname_id', instance.indexing_creator_orgname_id)
        instance.creator_orgname = validated_data.get(
            'creator_orgname', instance.creator_orgname)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.save()
        return instance


class IndexingPublisherDocumentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_publisher_document
        fields = ('indexing_publisher_id',
                  'publisher',
                  'frequency')

    def create(self, validated_data):
        return Indexing_publisher_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.indexing_publisher_id = validated_data.get(
            'indexing_publisher_id', instance.indexing_publisher_id)
        instance.publisher = validated_data.get(
            'publisher', instance.publisher)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.save()
        return instance


class IndexingPublisherEmailDocumentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Indexing_publisher_email_document
        fields = ('indexing_publisher_email_id',
                  'publisher_email',
                  'frequency')

    def create(self, validated_data):
        return Indexing_publisher_email_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.indexing_publisher_email_id = validated_data.get(
            'indexing_publisher_email_id', instance.indexing_publisher_email_id)
        instance.publisher_email = validated_data.get(
            'publisher_email', instance.publisher_email)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.save()
        return instance


class IndexingIssuedDateDocumentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Indexing_issued_date_document
        fields = ('indexing_issued_date_id',
                  'issued_date',
                  'frequency',)

    def create(self, validated_data):
        return Indexing_issued_date_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.indexing_issued_date_id = validated_data.get(
            'indexing_issued_date_id', instance.indexing_issued_date_id)
        instance.issued_date = validated_data.get(
            'issued_date', instance.issued_date)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.save()
        return instance
