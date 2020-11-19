from django.db import models

# Create your models here.

# dc_keyword table


class Dc_keyword(models.Model):
    DC_keyword_id = models.AutoField(primary_key=True)
    DC_keyword = models.CharField(max_length=191)
    index_document_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = "dc_keyword"

# dc_relation table


class Dc_relation(models.Model):
    DC_relation_id = models.AutoField(primary_key=True)
    DC_relation = models.CharField(max_length=191)
    index_document_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = "dc_relation"

# dc_type table


class Dc_type(models.Model):
    DC_type_id = models.AutoField(primary_key=True)
    DC_type = models.CharField(max_length=191)
    index_document_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = "dc_type"

# document table


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=191)
    version = models.IntegerField()
    path = models.TextField()
    DC_title = models.CharField(max_length=191)
    DC_title_alternative = models.CharField(max_length=191)
    DC_description_table_of_contents = models.TextField()
    DC_description_summary_or_abstract = models.TextField()
    DC_description_note = models.TextField()
    DC_format = models.CharField(max_length=191)
    DC_format_extent = models.CharField(max_length=191)
    DC_identifier_URL = models.CharField(max_length=191)
    DC_identifier_ISBN = models.CharField(max_length=191)
    DC_source = models.CharField(max_length=191)
    DC_language = models.CharField(max_length=191)
    DC_coverage_spatial = models.CharField(max_length=191)
    DC_coverage_temporal = models.CharField(max_length=191)
    DC_rights = models.CharField(max_length=191)
    DC_rights_access = models.CharField(max_length=191)
    thesis_degree_name = models.CharField(max_length=191)
    thesis_degree_level = models.CharField(max_length=191)
    thesis_degree_discipline = models.CharField(max_length=191)
    thesis_degree_grantor = models.CharField(max_length=191)
    rec_create_at = models.DateTimeField(auto_now=True)
    rec_create_by = models.CharField(max_length=191)
    rec_modified_at = models.DateTimeField(auto_now=True)
    rec_modified_by = models.CharField(max_length=191)
    index_creator = models.IntegerField(db_index=True)
    index_creator_orgname = models.IntegerField(db_index=True)
    index_publisher = models.IntegerField(db_index=True)
    index_contributor = models.IntegerField(db_index=True)
    index_issued_date = models.IntegerField(db_index=True)

    class Meta:
        db_table = "document"

# indexing_contributor_document table


class Indexing_contributor_document(models.Model):
    indexing_contributor_id = models.AutoField(primary_key=True)
    contributor = models.CharField(max_length=191)
    contributor_role = models.CharField(max_length=191)
    frequency = models.IntegerField()

    class Meta:
        db_table = "indexing_contributor_document"

# indexing_creator_document table


class Indexing_creator_document(models.Model):
    indexing_creator_id = models.AutoField(primary_key=True)
    creator = models.CharField(max_length=191)
    frequency = models.IntegerField()

    class Meta:
        db_table = "indexing_creator_document"

# indexing_creator_orgname_document table


class Indexing_creator_orgname_document(models.Model):
    indexing_creator_orgname_id = models.AutoField(primary_key=True)
    creator_orgname = models.CharField(max_length=191)
    frequency = models.IntegerField()

    class Meta:
        db_table = "indexing_creator_orgname_document"

# indexing_publisher_document table


class Indexing_publisher_document(models.Model):
    indexing_publisher_id = models.AutoField(primary_key=True)
    publisher = models.CharField(max_length=191)
    publisher_email = models.CharField(max_length=191)
    frequency = models.IntegerField()

    class Meta:
        db_table = "indexing_publisher_document"

# indexing_publish_date_document


class Indexing_issued_date_document(models.Model):
    indexing_issued_date_id = models.AutoField(primary_key=True)
    issued_date = models.DateField(
        auto_now_add=False, auto_now=False, null=True)
    frequency = models.IntegerField()

    class Meta:
        db_table = "indexing_issued_date_document"

# score table


class Score(models.Model):
    score_id = models.AutoField(primary_key=True)
    score_tf = models.DecimalField(max_digits=255, decimal_places=4)
    score_tf_idf = models.DecimalField(max_digits=255, decimal_places=4)
    index_term_word_id = models.IntegerField(db_index=True)
    index_document_id = models.IntegerField(db_index=True)
    generate_by = models.CharField(
        max_length=191, null=False, default="default")
    rec_status = models.IntegerField(null=False, default=1)

    class Meta:
        db_table = "score"

# term_word table


class Term_word(models.Model):
    term_word_id = models.AutoField(primary_key=True)
    term = models.CharField(max_length=191)
    frequency = models.IntegerField()
    score_idf = models.DecimalField(max_digits=255, decimal_places=4)
    rec_create_at = models.DateTimeField(auto_now=True)
    rec_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "term_word"


class Django_log(models.Model):
    django_log_id = models.AutoField(primary_key=True)
    rec_status = models.IntegerField()
    rec_create_date = models.DateTimeField(auto_now=True)
    log_error = models.CharField(max_length=191)
    index_document = models.IntegerField()

    class Meta:
        db_table = "django_log"
