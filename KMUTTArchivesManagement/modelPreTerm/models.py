from django.db import models

# Page_in_document Model


class Page_in_document(models.Model):
    page_in_document_id = models.AutoField(primary_key=True)
    page_index = models.IntegerField()
    name = models.CharField(max_length=191)
    rec_status_confirm = models.IntegerField()
    index_document_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = "page_in_document"


# Pre_term_in_page Model

class Pre_term_in_page(models.Model):
    pre_term_in_page_id = models.AutoField(primary_key=True)
    pre_term = models.CharField(max_length=191)
    index_page_in_document_id = models.IntegerField(db_index=True)

    class Meta:
        db_table = "pre_term_in_page"
