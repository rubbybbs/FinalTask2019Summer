from django.db import models

# Create your models here.

from django.db import models


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, default='')
    time = models.CharField(max_length=100, default='')
    original_url = models.CharField(max_length=100, default='')
    processed_url1 = models.CharField(max_length=100, default='')
    processed_url2 = models.CharField(max_length=100, default='')


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='')
