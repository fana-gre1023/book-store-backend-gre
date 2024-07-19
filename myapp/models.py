from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    coverurl = models.TextField()
    rate = models.FloatField()