from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
# foreign key relationship with user and restaurant models defined here
# this allows each review to be linked to a specific user and specific restaurant
# the related_name attribute names these connections allowing them to be easily referred to and accessed by the other side of the relationship(accessing reviews in User model and Restaurant model) - this allows related name of reviews to be passed to User and Restaurant models that can be used as fields inside the parent serializer if another serializer is created to define which fields from Review model are needed in User and Restaurant models
# with related_name relationship established, i can access all reviews written by a user(user.reviews) and all reviews for a particular restaurant(restaurant.reviews)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)