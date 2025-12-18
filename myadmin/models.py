from django.db import models

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=50,unique=True)
    caticon=models.CharField(max_length=100)

class SubCategory(models.Model):
    subcatid=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=50)
    subcatname=models.CharField(max_length=50,unique=True)
    subcaticon=models.CharField(max_length=100)
