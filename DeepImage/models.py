from django.db import models

# Create your models here.

from django.db import models


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.BigIntegerField()
