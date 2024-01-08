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

    # ? fk fields stay as fk fields in reviews because it captures the individual reviews with fk relationships for "User" and "Restaurant" aka each review can only have 1 user and 1 restaurant 

    # The 'users' field establishes a ManyToMany relationship with the User model through the Review model - needed as field here because the Restaurant table in ERD is one side of the many to many relationship with User
    # This relationship allows for the association of a restaurant with multiple users based on their reviews aka multiple users can leave a review for the same restaurant
    # The 'related_name' 'restaurant_reviews' is used to access all reviews associated with a restaurant from the User model and can be used as field for serialization in User model
    users = models.ManyToManyField(User, through="Review", related_name="restaurant_reviews")

    #the 'favorites' field creates a ManyToMany relationship between the Restaurant and User models through the Favorite model - each user can favorite multiple restaurants and a restaurant can be favorited by multiple users
    # This enables the tracking of which users have favorited a restaurant.
    # The 'related_name' 'favorite_restaurants' allows access to all favorited restaurants of a user and can be used as field during user model serialization
    favorites = models.ManyToManyField(User, through="Favorite", related_name="favorite_restaurants")