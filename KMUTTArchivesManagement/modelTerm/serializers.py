from rest_framework import serializers
from modelTerm.models import *


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

    def create(self, validated_data):
        return Score.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.score_id = validated_data.get('score_id', instance.score_id)
        instance.score_tf = validated_data.get('score_tf', instance.score_tf)
        instance.score_tf_idf = validated_data.get(
            'score_tf_idf', instance.score_tf_idf)
        instance.index_term_word_id = validated_data.get(
            'index_term_word_id', instance.index_term_word_id)
        instance.index_document_id = validated_data.get(
            'index_document_id', instance.index_document_id)
        instance.generate_by = validated_data.get(
            'generate_by', instance.generate_by)
        instance.rec_status = validated_data.get(
            'rec_status', instance.rec_status)
        instance.save()
        return instance


class TermWordSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Term_word
        fields = ('term_word_id',
                  'term',
                  'frequency',
                  'score_idf',
                  'rec_create_at',
                  'rec_modified_at')

    def create(self, validated_data):
        return Term_word.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.term_word_id = validated_data.get(
            'term_word_id', instance.term_word_id)
        instance.term = validated_data.get('term', instance.term)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.score_idf = validated_data.get(
            'score_idf', instance.score_idf)
        instance.rec_create_at = validated_data.get(
            'rec_create_at', instance.rec_create_at)
        instance.rec_modified_at = validated_data.get(
            'rec_modified_at', instance.rec_modified_at)
        instance.save()
        return instance
