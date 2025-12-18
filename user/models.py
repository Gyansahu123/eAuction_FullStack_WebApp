from django.db import models
from myadmin.models import Category, SubCategory
from django.contrib.auth.models import User

# Create your models here.

class Funds(models.Model):
    txnid=models.AutoField(primary_key=True)
    uid=models.CharField(max_length=50)
    amt=models.IntegerField()
    info=models.CharField(max_length=50)





class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    categoryname = models.CharField(max_length=50)   # ✅ new field
    subcatname = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    baseprice = models.IntegerField()
    picon = models.ImageField(upload_to="products/")
    uid = models.CharField(max_length=50)
    info = models.CharField(max_length=50)





class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")
    bidder_id = models.CharField(max_length=50, default="guest")
    bidder_name = models.CharField(max_length=100, blank=True)
    bidder_email = models.CharField(max_length=100, default="anonymous@example.com")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bid_time = models.DateTimeField(auto_now_add=True)