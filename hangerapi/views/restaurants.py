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
            # Restaurant,objects.all() makes query that retrieves all instances of the Restaurant model from the database - then stored in restaurants variable
            # restaurants variable then used as parameter for proper serializer(RestaurantSerializer) many=True argument lets serializer know there will be multiple instances
            # result of serialized data stored in serializer variable to be used in Response so proper JSON format can be sent to front end and displayed
            # with response status to indicate success
            restaurants = Restaurant.objects.all()
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        def retrieve(self, request, pk=None):
            """Handle GET requests for a single restaurant
        
        Returns:
            Response -- JSON serialized restaurant object
            """

            # A GET request is made to retrieve a single Restaurant instance based on the provided primary key (pk)
            # if Restaurant instance matching pk found, it's serialized
            # if no matching pk found, Restaurant.DoesNotExist exception caught and error message shown in response
            # context parameter used to pass additional information to a serializer that it might need to correctly serialize or deserialize data
            # The context is a dictionary that can be passed to a serializer upon its instantiation.
            # It's typically used to provide data that is not part of the model instance being serialized but is still necessary for the serialization process
            # In retrieve method, passing context={"request": request} to the RestaurantSerializer
            # This means inside RestaurantSerializer, you can access the request object using self.context['request']
            # This access to the request object can be used to tailor the serialized data according to the current user (the user who sent the request) -ie what is rendered can be altered to fit current user or user status
            try:
                restaurant = Restaurant.objects.get(pk=pk)
                reviews = restaurant.reviews.all().order_by('-date')
                serializer = RestaurantSerializer(restaurant, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Restaurant.DoesNotExist as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
