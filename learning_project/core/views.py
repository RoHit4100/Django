from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json
from django.core.paginator import Paginator, PageNotAnInteger
from .models import Restaurant, Sale, User, Rating
import requests
from .constants import *
from .common_functions import *
from .constants import *

@csrf_exempt
def registration(request):
    # here I will get the data related to the user
    try: 
        if request.method == 'POST':
            # get the data for the username and the password with the email
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            if not email or not username or not password:
                return JsonResponse({'error': 'all fields are required'})
            
            # create the user
            user = User.objects.create_user(username=username, email=email, password=password) # this will create user with hashing

            send_welcome_email(email, username)
            return JsonResponse({'message': 'User successfully created'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def createRestaurant(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            
            name = data.get(RESTAURANT_NAME)
            website = data.get(RESTAURANT_WEBSITE, '')
            date_opened = data.get(RESTAURANT_DATE_OPENED, datetime.today().date())
            latitude = data.get(RESTAURANT_LATITUDE)
            longitude = data.get(RESTAURANT_LONGITUDE)
            restaurant_type = data.get(RESTAURANT_TYPE)
            
            if not name or latitude is None or longitude is None or not restaurant_type:
                return JsonResponse({'error': 'missing values'}, status=HTTP_STATUS_BAD_REQUEST)
            
            restaurant = Restaurant(
                name=name,
                website=website,
                date_opened=date_opened,
                latitude=latitude,
                longitude=longitude,
                restaurant_type=restaurant_type
            )
            restaurant.save()
            return JsonResponse({'message': 'Restaurant successfully added!'}, status=HTTP_STATUS_CREATED)
        else:
            return JsonResponse({'error': 'Only POST methods are allowed'}, status=HTTP_STATUS_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_STATUS_BAD_REQUEST)

@csrf_exempt
def createRating(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            restaurant_id = request.POST.get('restaurant_id')

            # get the user and restuarant associated with those id's
            user = User.objects.get(id=user_id)
            restaurant = Restaurant.objects.get(id=restaurant_id)
            
            data = json.loads(request.body)
            rating = data.get(RATING_VALUE)
            review = data.get(RATING_REVIEW, '')
            
            if not user_id or rating is None:
                return JsonResponse({'error': 'User and rating are required'}, status=HTTP_STATUS_BAD_REQUEST)
            
            rating_entry = Rating(
                user=user,
                restaurant=restaurant,
                rating=rating,
                review=review
            )
            rating_entry.save()
            return JsonResponse({'message': 'Rating successfully added!'}, status=HTTP_STATUS_CREATED)
        else:
            return JsonResponse({'error': 'Only POST methods are allowed'}, status=HTTP_STATUS_BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=HTTP_STATUS_BAD_REQUEST)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=HTTP_STATUS_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_STATUS_BAD_REQUEST)

@csrf_exempt
def createSale(request):
    try:
        if request.method == 'POST':
            restaurant_id = request.POST.get('restaurant_id')
            restaurant = Restaurant.objects.get(id=restaurant_id)
            
            
            data = json.loads(request.body)
            income = data.get(SALE_INCOME)
            date_time = data.get(SALE_DATE_TIME)
            
            if income is None or date_time is None:
                return JsonResponse({'error': 'Income and date time are required'}, status=HTTP_STATUS_BAD_REQUEST)
            
            sale_entry = Sale(
                restaurant=restaurant,
                income=income,
                date_time=date_time
            )
            sale_entry.save()
            return JsonResponse({'message': 'Sale successfully added!'}, status=HTTP_STATUS_CREATED)
        else:
            return JsonResponse({'error': 'Only POST methods are allowed'}, status=HTTP_STATUS_BAD_REQUEST)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=HTTP_STATUS_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_STATUS_BAD_REQUEST)
    
def getRestaurants(request):
    try: 
        if request.method == "GET":
            sort_by = request.GET.get('sort', 'id')

            # Validate sort_by against valid fields
            valid_sort_fields = ['id', 'name', 'date_opened', 'restaurant_type']  # add other fields as needed
            if sort_by not in valid_sort_fields:
                return JsonResponse({'error': f'Invalid sort field: {sort_by}'}, status=HTTP_STATUS_BAD_REQUEST)

            restaurants = Restaurant.objects.order_by(sort_by).values()
            return JsonResponse(list(restaurants), safe=False)
        else:
            return JsonResponse({'error': 'Only GET methods are allowed'}, status=HTTP_STATUS_BAD_REQUEST)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_STATUS_BAD_REQUEST)
    
def getRestaurant(request):
    try:
        if request.method == 'GET':
            # get the field name and the value, for that particular field
            field = request.GET.get('field')
            value = request.GET.get('value')
            
            if not field or not value:
                return JsonResponse({'error': 'Missing Values'}, status=HTTP_STATUS_BAD_REQUEST)
            
            # now perform the validation for the field
            if field not in ['id', 'name', 'website', 'date_opened', 'longitude', 'latitude', 'restaurant_type']:
                return JsonResponse({'error': 'Not valid field'}, status=HTTP_STATUS_BAD_REQUEST)

            restaurant = Restaurant.objects.filter(field=value)
            if not restaurant.exists():
                return JsonResponse({'error': 'There is nothing related to this field and the value'}, status=HTTP_STATUS_BAD_REQUEST)
            
            return JsonResponse(list(restaurant.values()), safe=False, status=HTTP_STATUS_OK)
        else:
            return JsonResponse({'error': 'Only GET methods are allowed'}, status=HTTP_STATUS_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=HTTP_STATUS_BAD_REQUEST)