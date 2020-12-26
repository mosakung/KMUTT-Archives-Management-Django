from django.db import models

# Score Model


class Score(models.Model):
    score_id = models.AutoField(primary_key=True)
    score_tf = models.DecimalField(
        null=False, max_digits=255, decimal_places=4)
    score_tf_idf = models.DecimalField(
        null=True, max_digits=255, decimal_places=4)
    index_term_word_id = models.IntegerField(null=False, db_index=True)
    index_document_id = models.IntegerField(null=False, db_index=True)
    generate_by = models.CharField(
        max_length=191, null=False, default="default")
    rec_status = models.IntegerField(null=False, default=1)

    class Meta:
        db_table = "score"

# Term_word Model


class Term_word(models.Model):
    term_word_id = models.AutoField(primary_key=True)
    term = models.CharField(null=False, max_length=191)
    frequency = models.IntegerField(null=False)
    score_idf = models.DecimalField(
        null=True, max_digits=255, decimal_places=4)
    rec_create_at = models.DateTimeField(auto_now=True)
    rec_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "term_word"
