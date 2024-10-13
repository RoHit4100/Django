from django.shortcuts import render
import json
from .models import Expense
from django.http import HttpResponse, JsonResponse



# Create your views here.
def createExpense(request):
    if request.method == 'POST':
        try:
            # convert the request body into json
            data = json.loads(request.body)
            # create new entry for the current post expense
            expense = Exception.object.create(
                title = data['title'],
                amount = data['amount'],
                date = data['date'],
                description = data.get('description', '')
            )

            return JsonResponse({'id': expense.id, 'message': 'Expense created successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
    return HttpResponse(status = 405)