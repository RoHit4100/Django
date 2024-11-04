from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.registration, name='registration'), 
    path('create-restaurant/', views.createRestaurant, name='createRestaurant'),
    path('create-rating/', views.createRating, name='createRating'),
    path('create-sale', views.createSale, name='createSale'),
    path('get-restaurants/', views.getRestaurants, name='getRestaurants'),  
    path('get-restaurant/', views.getRestaurant, name='getRestaurant'),
    path('get-ratings/', views.getRatingsForRestaurant, name='getRatings'),
    path('get-sales/', views.getSalesForRestaurant, name='getSalesForRestaurant'),
    path('get-restaurant-with-name/', views.getRestaurantWithName, name='getRestaurantWithName'),
    path('get-restaurant-with-type/', views.searchWithTypes, name='searchRestaruantWithType'),  
]

