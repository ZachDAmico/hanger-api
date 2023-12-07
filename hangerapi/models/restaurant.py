from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=155)
    location = models.CharField(max_length=155)
    price_range = models.ForeignKey("PriceRange", on_delete=models.CASCADE, related_name="restaurants")
    rating = models.IntegerField()
    hanger_level = models.IntegerField()
    cuisine = models.ForeignKey("Cuisine", on_delete=models.CASCADE, related_name="restaurants")
    img_url = models.CharField(max_length=200)
    # fk fields stay the same in reviews because it captures the individual reviews with fk relationships for "User" and "Restaurant"
    # user_reviews is needed as ManyToManyField to retrieve all reviews written by specific user for any restaurant and all reviews for specific restaurant
    users = models.ManyToManyField(User, through="Review", related_name="restaurant_reviews")