
from django.db import models


class Bestdeal(models.Model):
    price = models.IntegerField()
    category = models.CharField(max_length=255, blank=True, null=True)
    prev_price = models.IntegerField(blank=True, null=True)
    item_link = models.CharField(max_length=255, blank=True, null=True)
    image_src = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    per_discount = models.IntegerField(blank=True, null=True)
    sub_category = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        db_table = 'bestdeal'
        ordering=['sub_category','category']
