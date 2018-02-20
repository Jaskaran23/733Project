from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Page(models.Model):
    # URL Info
    url        = models.TextField()
    domain     = models.TextField()
    path       = models.TextField()

    # Rank Info
    rank       = models.IntegerField()
    in_links   = ArrayField(models.TextField())

    # Data Fields
    out_links  = ArrayField(models.TextField())
    text       = models.TextField()
    images     = ArrayField(models.ImageField())
    tags       = ArrayField(models.TextField())
    currencies = ArrayField(models.TextField())
    sentiment  = models.IntegerField()
