from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    # i've defined a ForeignKey relationship with the User model and a ForeignKey relationship with the Restaurant model. The related_name parameter allows access to the related reviews from both the user and the restaurant. this essentially passes the related name to be potentially serialized in user or restaurant and used as a field 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)