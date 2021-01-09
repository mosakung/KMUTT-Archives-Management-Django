from django.db import models

# Document Model


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    status_process_document = models.IntegerField(null=False, default=0)
    name = models.CharField(null=False, max_length=191)
    version = models.IntegerField(null=False)
    page_start = models.IntegerField(null=False)
    amount_page = models.IntegerField(null=False, default=0)
    path = models.TextField(null=False)
    path_image = models.TextField(null=False)
    DC_title = models.CharField(null=False, max_length=191)
    DC_title_alternative = models.CharField(null=True, max_length=191)
    DC_description_table_of_contents = models.TextField(null=True)
    DC_description_summary_or_abstract = models.TextField(null=True)
    DC_description_note = models.TextField(null=True)
    DC_format = models.CharField(null=True, max_length=191)
    DC_format_extent = models.CharField(null=True, max_length=191)
    DC_identifier_URL = models.CharField(null=True, max_length=191)
    DC_identifier_ISBN = models.CharField(null=True, max_length=191)
    DC_source = models.CharField(null=True, max_length=191)
    DC_language = models.CharField(null=True, max_length=191)
    DC_coverage_spatial = models.CharField(null=True, max_length=191)
    DC_coverage_temporal = models.CharField(null=True, max_length=191)
    DC_coverage_temporal_year = models.CharField(null=True, max_length=191)
    DC_rights = models.CharField(null=True, max_length=191)
    DC_rights_access = models.CharField(null=True, max_length=191)
    thesis_degree_name = models.CharField(null=True, max_length=191)
    thesis_degree_level = models.CharField(null=True, max_length=191)
    thesis_degree_discipline = models.CharField(null=True, max_length=191)
    thesis_degree_grantor = models.CharField(null=True, max_length=191)
    rec_create_at = models.DateTimeField(null=False, auto_now=True)
    rec_create_by = models.IntegerField(null=False, db_index=True)
    rec_modified_at = models.DateTimeField(null=False, auto_now=True)
    rec_modified_by = models.IntegerField(null=False, db_index=True)
    index_creator = models.IntegerField(null=True, db_index=True)
    index_creator_orgname = models.IntegerField(null=True, db_index=True)
    index_publisher = models.IntegerField(null=True, db_index=True)
    index_contributor = models.IntegerField(null=True, db_index=True)
    index_issued_date = models.IntegerField(null=True, db_index=True)

    class Meta:
        db_table = "document"

# Dc_keyword Model


class Dc_keyword(models.Model):
    DC_keyword_id = models.AutoField(primary_key=True)
    DC_keyword = models.CharField(null=False, max_length=191)
    index_document_id = models.IntegerField(null=False, db_index=True)

    class Meta:
        db_table = "dc_keyword"

# Dc_relation Model


class Dc_relation(models.Model):
    DC_relation_id = models.AutoField(primary_key=True)
    DC_relation = models.CharField(null=False, max_length=191)
    index_document_id = models.IntegerField(null=False, db_index=True)

    class Meta:
        db_table = "dc_relation"

# Dc_type Model


class Dc_type(models.Model):
    DC_type_id = models.AutoField(primary_key=True)
    DC_type = models.CharField(null=False, max_length=191)
    index_document_id = models.IntegerField(null=False, db_index=True)

    class Meta:
        db_table = "dc_type"

# Indexing_contributor_document Model


class Indexing_contributor_document(models.Model):
    indexing_contributor_id = models.AutoField(primary_key=True)
    contributor = models.CharField(null=False, max_length=191)
    contributor_role = models.CharField(null=True, max_length=191)
    frequency = models.IntegerField(null=False)

    class Meta:
        db_table = "indexing_contributor_document"

# Indexing_creator_document Model


class Indexing_creator_document(models.Model):
    indexing_creator_id = models.AutoField(primary_key=True)
    creator = models.CharField(null=False, max_length=191)
    frequency = models.IntegerField(null=False)

    class Meta:
        db_table = "indexing_creator_document"

# Indexing_creator_orgname_document Model


class Indexing_creator_orgname_document(models.Model):
    indexing_creator_orgname_id = models.AutoField(primary_key=True)
    creator_orgname = models.CharField(null=False, max_length=191)
    frequency = models.IntegerField(null=False)

    class Meta:
        db_table = "indexing_creator_orgname_document"

# Indexing_publisher_document Model


class Indexing_publisher_document(models.Model):
    indexing_publisher_id = models.AutoField(primary_key=True)
    publisher = models.CharField(null=False, max_length=191)
    publisher_email = models.CharField(null=True, max_length=191)
    frequency = models.IntegerField(null=False,)

    class Meta:
        db_table = "indexing_publisher_document"

# Indexing_issued_date_document Model


class Indexing_issued_date_document(models.Model):
    indexing_issued_date_id = models.AutoField(primary_key=True)
    issued_date = models.DateField(
        auto_now_add=False, auto_now=False, null=False)
    frequency = models.IntegerField(null=False)

    class Meta:
        db_table = "indexing_issued_date_document"
