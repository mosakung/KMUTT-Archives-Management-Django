from rest_framework import serializers
from modelPreTerm.models import *


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


class PageInDocumentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Page_in_document
        fields = ('page_in_document_id',
                  'page_index',
                  'name',
                  'rec_status_confirm',
                  'index_document_id')

    def create(self, validated_data):
        return Page_in_document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.page_in_document_id = validated_data.get(
            'page_in_document_id', instance.page_in_document_id)
        instance.page_index = validated_data.get(
            'page_index', instance.page_index)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.rec_status_confirm = validated_data.get(
            'rec_status_confirm', instance.rec_status_confirm)
        instance.index_document_id = validated_data.get(
            'index_document_id', instance.index_document_id)
        instance.save()
        return instance


class PreTermInPageSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Pre_term_in_page
        fields = ('pre_term_in_page_id',
                  'pre_term',
                  'index_page_in_document_id')

    def create(self, validated_data):
        return Pre_term_in_page.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.pre_term_in_page_id = validated_data.get(
            'pre_term_in_page_id', instance.pre_term_in_page_id)
        instance.pre_term = validated_data.get(
            'pre_term', instance.pre_term)
        instance.index_page_in_document_id = validated_data.get(
            'index_page_in_document_id', instance.index_page_in_document_id)
        instance.save()
        return instance
