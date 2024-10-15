import json
from .models import Expense
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def expenseList(request):
    # check if the request is GET or POST method
    if request.method == 'GET':
        # Retrieve all expenses and return as a JSON response
        # print(request.GET)
        operation = request.GET.get('sort') # by default function will be in ascending order
        target = request.GET.get('on')
        
        if operation == 'asc': # perform ascending operations
            # print('asc')
            # check the target
            if target == 'date': # target is date
                expense = Expense.objects.order_by('date').values('id', 'title', 'amount', 'date')[:10]
                return JsonResponse(list(expense), safe=False)   
            elif target == 'amount':
                expense = Expense.objects.order_by('amount').values('id', 'title', 'amount', 'date')
                return JsonResponse(list(expense), safe=False)
            elif target == 'title':
                expense = Expense.objects.order_by('title').values('id', 'title', 'amount', 'date')
                return JsonResponse(list(expense), safe=False)
            
        elif operation == 'desc':
            # print('desc')
            if target == 'date': # target is date
                expense = Expense.objects.order_by('-date').values('id', 'title', 'amount', 'date')
                return JsonResponse(list(expense), safe=False)   
            elif target == 'amount':
                expense = Expense.objects.order_by('-amount').values('id', 'title', 'amount', 'date')
                return JsonResponse(list(expense), safe=False)
            elif target == 'title':
                expense = Expense.objects.order_by('-title').values('id', 'title', 'amount', 'date')
                return JsonResponse(list(expense), safe=False)
        else:
            # print('default')
            expenses = Expense.objects.all().values('id', 'title', 'amount', 'date')
            return JsonResponse(list(expenses), safe=False)  # safe=False means data is not a dictionary

    elif request.method == 'POST':  # Adding feature to handle bulk data
        data = json.loads(request.body)  # Parse JSON string into a Python object

        # Check if the data is a list (for bulk insert)
        if isinstance(data, list):
            expenses = []
            for item in data:
                title = item.get('title')
                amount = item.get('amount')
                date = item.get('date')
                # Validate if any data is absent
                if not title or not amount or not date:
                    return JsonResponse({'error': 'Missing values'}, status=400)

                # Create new Expense instance and add to the list
                expenses.append(Expense(title=title, amount=amount, date=date))
            
            # Perform bulk insert
            Expense.objects.bulk_create(expenses)
            return JsonResponse({'message': 'Expenses added successfully'}, status=201)

        # Handle single data entry
        else:
            title = data.get('title')
            amount = data.get('amount')
            date = data.get('date')

            # Validate data
            if not title or not amount or not date:
                return JsonResponse({'error': 'Missing values'}, status=400)

            # Create new Expense instance
            expense = Expense.objects.create(title=title, amount=amount, date=date)
            return JsonResponse({'message': 'Expense added successfully.', 'id': expense.id}, status=201)

@csrf_exempt
def expenseDetail(request, pk):
    try: # first check if the id exists or not
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return JsonResponse({'error': 'Expense doest not exists'}, status=404)
    
    # for get request
    if request.method == 'GET':
        # print(dict(request.GET))
        return JsonResponse({'id': expense.id, 'title': expense.title, 'amount': expense.amount, 'date': expense.date})
    
    # for update request
    elif request.method == 'PUT':
        try:
            # first get the data present in the body
            data = json.loads(request.body)
            # get the data which user wants to update
            expense.title = data.get('title', expense.title)
            expense.amount = data.get('amount', expense.amount)
            expense.date = data.get('date', expense.date)
            
            # save the expense
            expense.save()
            return JsonResponse({'message': 'Expense is succesfully updated'})
        except Exception as e: 
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        expense.delete()
        return JsonResponse({'message': 'Expense successfully deleted'})
        
@csrf_exempt
def expenseQuery(request):
    if request.method == 'GET':
        query = request.GET.get('title', '') 
        date = request.GET.get('date', '') 
        amount = request.GET.get('amount', '')


        if query or date or amount:
            expenses = Expense.objects.filter(title__icontains=query, amount__icontains=amount, date__icontains=date).values()
        else:
            expenses = Expense.objects.all().values()

        return JsonResponse(list(expenses), safe=False)

def expenseUnique(request):
    if request.method == 'GET':
        target = request.GET.get('target')
        col = ['title', 'amount', 'date']
        if target in col:
            expense = Expense.objects.order_by('-' + target).values(target).distinct()
            return JsonResponse(list(expense), safe=False)
        else:
            return JsonResponse({'message': 'Enter valid target field'})