from django.db import models

class PriceRange(models.Model):
    price_range = models.IntegerField()