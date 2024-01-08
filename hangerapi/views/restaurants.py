from rest_framework.viewsets import ViewSet
# from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from hangerapi.models import Restaurant
from .price_range import PriceRangeSerializer
from .cuisine import CuisineSerializer
from .reviews import ReviewSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    # saving serializers as variables same as fields so data from other corresponding table shows in this serializer
    # ie cuisine will show up as string name and not just integer when requested
    price_range = PriceRangeSerializer(many=False)
    cuisine = CuisineSerializer(many=False)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Restaurant
        # can be reviews because of related name from review model
        # removed rating from fields here because it's in review
        fields = ["id", "name", "location", "price_range", "hanger_level", "cuisine", "img_url", "reviews" ]

# ? REMINDER - functions inside Python classes are methods, ViewSets are Django related
class RestaurantView(ViewSet):

        def list(self, request):
            """Handle GET requests for the list of restaurants

        Returns:
            Response -- JSON serialized array of restaurants
        """
            restaurants = Restaurant.objects.all()
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        def retrieve(self, request, pk=None):
            """Handle GET requests for a single restaurant
        
        Returns:
            Response -- JSON serialized restaurant object
            """
            try:
                restaurant = Restaurant.objects.get(pk=pk)
                reviews = restaurant.reviews.all().order_by('-date')
                serializer = RestaurantSerializer(restaurant, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Restaurant.DoesNotExist as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
