from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json
import re
from django.core.paginator import Paginator, PageNotAnInteger
from .models import Restaurant, Sale, User, Rating
import requests
from requests.exceptions import RequestException
from datetime import datetime, timedelta
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
            return JsonResponse({'message': 'User successfully created'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# @csrf_exempt
# def createRestaurants(request):
    