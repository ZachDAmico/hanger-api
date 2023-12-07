from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from hangerapi.models import Review
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
                    serializer = ReviewSerializer(data=request.data, partial=True)
                    if serializer.is_valid():
                        review.rating = serializer.validated_data["rating"]
                        review.comment = serializer.validated_data["comment"]
                        review.save()

                        serializer = ReviewSerializer(review, context={'request': request})
                        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            except Review.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        def create(self, request):
            """Handle POST operations

        Returns
            Response -- JSON serialized review instance
        """
            serializer = ReviewSerializer(data=request.data)

            if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        

