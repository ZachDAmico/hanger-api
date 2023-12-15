from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .restaurants import Restaurant


class FavoriteRestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["name", "img_url"]
class UserSerializer(serializers.ModelSerializer):
    favorite_restaurants = FavoriteRestaurantSerializer(many=True)
   
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', "favorite_restaurants")  # add other fields as needed
        extra_kwargs = {'password': {'write_only': True}}

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                  

    @action(detail=False, methods=['post'], url_path='login')
    def user_login(self, request):
        '''Handles the authentication of a user

        Method arguments:
        request -- The full HTTP request object
        '''
        username = request.data['username']
        password = request.data['password']

        # Use the built-in authenticate method to verify
        # authenticate returns the user object or None if no user is found
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)

            data = {
                'valid': True,
                'token': token.key,
                'staff': token.user.is_staff,
                'id': token.user.id
            }
            return Response(data)
        else:
            # Bad login details were provided. So we can't log the user in.
            data = { 'valid': False }
            return Response(data)
        
    def list(self, request):
            """Handle GET requests for the list of users

        Returns:
            Response -- JSON serialized array of users
        """
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
            """Handle GET requests for a single user
        
        Returns:
            Response -- JSON serialized user object
            """
            try:
                review = User.objects.get(pk=pk)
                serializer = UserSerializer(review, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist as ex:
                return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)