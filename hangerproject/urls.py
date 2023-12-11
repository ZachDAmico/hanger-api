from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from hangerapi.views import UserViewSet, CuisineView, PriceRangeView, RestaurantView, ReviewView, FavoriteView

router = DefaultRouter(trailing_slash=False)
router.register(r'cuisines', CuisineView, 'cuisine')
router.register(r'price_ranges', PriceRangeView, 'price_range' )
router.register(r'restaurants', RestaurantView, 'restaurant' )
router.register(r'reviews', ReviewView, 'review' )
router.register(r'favorites', FavoriteView, 'favorite' )
router.register(r'users', UserViewSet, 'user' )


urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
]

