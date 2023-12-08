from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name="favorite_restaurant")