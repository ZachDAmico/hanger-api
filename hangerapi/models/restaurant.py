from django.db import models
# from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=155)
    location = models.CharField(max_length=155)
    price_range = models.ForeignKey("PriceRange", on_delete=models.CASCADE, related_name="restaurants")
    rating = models.IntegerField()
    hanger_level = models.IntegerField()
    cuisine = models.ForeignKey("Cuisine", on_delete=models.CASCADE, related_name="restaurants")
    img_url = models.CharField(max_length=200)