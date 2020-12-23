from django.db import models

# User Model


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(null=True, max_length=191)
    surname = models.CharField(null=True, max_length=191)
    role = models.CharField(null=False, max_length=191)
    username = models.CharField(null=False, max_length=191)
    password = models.CharField(null=True, max_length=191)
    create_at = models.DateTimeField(null=False, auto_now=True)
    active = models.IntegerField(null=False, default=1)

    class Meta:
        db_table = "user"
