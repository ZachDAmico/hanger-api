from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from hangerapi.models import Favorite, Restaurant


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["user", "restaurant"]

# class FavoriteRestaurantSerializer(ModelSerializer):
#     class Meta:
#         model = Restaurant
#         fields = ["name", "img_url"]


class FavoriteView(ViewSet):

    def create(self, request):
        """Handle POST operations for favorite

        Returns
            Response -- JSON serialized review instance
        """
        serializer = FavoriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
