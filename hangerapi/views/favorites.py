from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from hangerapi.models import Favorite, Restaurant
from django.shortcuts import get_object_or_404

# FavoriteRestaurantSerializer created because some restaurant fields are needed when favorite instance is serialized. then stored in FavoriteSerializer as variable called restaurant because that is the name of the field in the favorite model
class FavoriteRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["name", "img_url"]

# FavoriteSerializer is directly associated with the Favorite model. It tells the frontend which fields from the Favorite model are accessible. In this case, it's the user and restaurant
class FavoriteSerializer(ModelSerializer):
    restaurant = FavoriteRestaurantSerializer(many=False)
    class Meta:
        model = Favorite
        fields = ["user", "restaurant"]
class FavoriteView(ViewSet):
    def create(self, request):
        # Get user from the request (assuming token authentication)
        user = request.user
        # Get restaurant ID from the request
        restaurant_id = request.data.get('restaurant')
        # Retrieve the Restaurant instance using the provided primary key
        restaurant_instance = get_object_or_404(Restaurant, pk=restaurant_id)
        # Create Favorite instance associated with the user and the retrieved Restaurant instance
        create = Favorite.objects.create(
            user=user,
            restaurant=restaurant_instance
        )
        # Serialize and return the response
        serializer = FavoriteSerializer(create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def list(self, request):
        # Change variable name to 'favorites'
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single favorite
        Returns:
            Response -- empty response body
        """
        try:
            favorite = Favorite.objects.get(pk=pk)
            if request.user.id == favorite.user_id:
                favorite.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "This is not your favorite."}, status=status.HTTP_403_FORBIDDEN)
        except Favorite.DoesNotExist as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

