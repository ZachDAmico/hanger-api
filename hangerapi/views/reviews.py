from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from hangerapi.models import Review, Restaurant
from django.contrib.auth.models import User

class UserReviewSerializer(ModelSerializer):

    class Meta: 
        model = User
        fields = ["id", "username"]
class ReviewSerializer(ModelSerializer):
    user = UserReviewSerializer(many=False)
    
    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "date" ]

class ReviewView(ViewSet):

        def list(self, request):
            """Handle GET requests for the list of reviews

        Returns:
            Response -- JSON serialized array of reviews
        """
            reviews = Review.objects.all().order_by('-date')
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

        def retrieve(self, request, pk=None):
            """Handle GET requests for a single review
        
        Returns:
            Response -- JSON serialized review object
            """
            try:
                review = Review.objects.get(pk=pk)
                serializer = ReviewSerializer(review, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Review.DoesNotExist as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
        def destroy(self, request, pk=None):
            """Handle DELETE requests for a single review

        Returns:
            Response -- empty response body
        """
            try:
                review = Review.objects.get(pk=pk)
                #  request.user is object that represents user making current request and this is grabbing the id key
                # review.user_id is looking at the review table of the database and looking to see if the user_id(it's user_id despite being "user" in serializer)matches the user.id from request
                if request.user.id == review.user_id:
                    review.delete()
                    return Response(None, status=status.HTTP_204_NO_CONTENT)
                return Response({"message": "You are not the author of this review."}, status=status.HTTP_403_FORBIDDEN)
            except Review.DoesNotExist as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
            except Exception as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        def update(self, request, pk=None):
            """Handle PUT requests for a single review

        Returns:
            Response -- JSON serialized object
            """
            try:
                review = Review.objects.get(pk=pk)
                if request.user.id == review.user_id:
                    # This line creates an instance of the ReviewSerializer with the data sent in       the request (request.data).
                            # partial=True indicates that a partial update is allowed. This means not all fields of the serializer need to be present in the request data for the serializer to consider it valid. This is useful for PUT requests where you might only want to update a subset of fields.
                    serializer = ReviewSerializer(data=request.data, partial=True)
                    # This line checks if the data provided in the request is valid according to the rules defined in the ReviewSerializer. It validates the data against the serializer's
                    # fields and their respective validation rules. If the data passes all validations, the method proceeds; otherwise, it would typically return a response indicating what was invalid.
                    if serializer.is_valid():
                        # serializer.validated_data is a dictionary containing the data that was validated and processed by the serializer. This data is considered safe to use and save to the database - rating and comment designate where data is to be assigned
                        review.rating = serializer.validated_data["rating"]
                        review.comment = serializer.validated_data["comment"]
                        # saves changes to database
                        review.save()
                    # then serializes updated review and returns in response 
                        serializer = ReviewSerializer(review, context={'request': request})
                        # A new instance of ReviewSerializer is created, this time passing the updated review object itself (not the request data)
                        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            except Review.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        def create(self, request):
            """Handle POST operations

        Returns
            Response -- JSON serialized review instance
        """
            
            # ? this was original create method
            # ? this made postman require dictionary for user key, but would not allow for username to be a name that already exists

            # serializer = ReviewSerializer(data=request.data)

            # if serializer.is_valid():
            #  serializer.save()
            #  return Response(serializer.data, status=status.HTTP_201_CREATED)
            # else:
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # ? so need to dynamically define the request body to expect what is needed - ie comment and rating

            try:
                # ? overall, this is extracting data from the user's request and saving it in variables to be used in the Review.objects.create
                # refers to the currently authenticated user
                user = request.user
                # This extracts the rating value from the request data
                rating = request.data.get("rating")
                # This extracts the comment value from the request data
                comment = request.data.get("comment")
                # This retrieves the restaurant_id from the request data
                # needed to identify which specific restaurant the review is associated with aka user's input specifying which restaurant instance the review is for
                restaurant_id = request.data.get("restaurant_id")
                # this line fetches the corresponding Restaurant instance from the database. It uses the primary key lookup to get the specific Restaurant object that matches the restaurant_id
                # using the restaurant_id fetch the actual restaurant object from the database
                # This step is necessary because Review model needs a reference to an actual Restaurant instance, not just an ID. The ForeignKey relationship in Review model requires an instance of the Restaurant model
                restaurant = Restaurant.objects.get(pk=restaurant_id)

# This line creates a new Review instance in the database. The create method is a shortcut for creating a new instance with the given data and immediately saving it to the database.
# The Review instance is created with the extracted user, rating, comment, and the fetched restaurant instance
                review = Review.objects.create(
                    user = user,
                    rating = rating,
                    comment = comment,
                    restaurant = restaurant,
                )
                # After successfully creating the Review instance, it is then serialized using ReviewSerializer
                serializer = ReviewSerializer(review, context={"request": request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as ex:
                return Response(ex, status=status.HTTP_400_BAD_REQUEST)
