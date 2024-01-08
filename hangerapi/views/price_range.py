from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from hangerapi.models import PriceRange

# price_range break point most likely triggered first because Django looks for nest data first and the landing page makes GET request for all restaurants. price_range is first piece of nested data in that request
class PriceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRange
        fields = ["id", "price_range"]

class PriceRangeView(ViewSet):
    def list(self, request):
        """Handle GET requests for the list of price_ranges

        Returns:
            Response -- JSON serialized array of price_ranges
        """
        price_ranges= PriceRange.objects.all()
        serializer = PriceRangeSerializer(price_ranges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # pk=None used to tell django that if no pk is provided, value defaults to None
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single price_range
        
        Returns:
            Response -- JSON serialized price_range object
            """
        try:
            price_range = PriceRange.objects.get(pk=pk)
            serializer = PriceRangeSerializer(price_range, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PriceRange.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)