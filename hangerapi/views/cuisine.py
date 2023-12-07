from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from hangerapi.models import Cuisine

# serializers convert models from database into python json so they need to include all needed fields
# basically defines what you want to see when you make the request from the model
class CuisineSerializer(ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ["id", "type"]

# view methods contain request type, the serialization of data returned, and response expected
class CuisineView(ViewSet):
    def list(self, request):
        """Handle GET requests for the list of cuisines

        Returns:
            Response -- JSON serialized array of cuisines
        """
        cuisines = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # pk=None used to tell django that if no pk is provided, value defaults to None
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single cuisine

        Returns:
            Response -- JSON serialized cuisine object
            """
        try:
            # many= defaults to false unless explicitly stated
            cuisine = Cuisine.objects.get(pk=pk)
            serializer = CuisineSerializer(cuisine, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cuisine.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)