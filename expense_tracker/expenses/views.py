import json
from .models import Expense
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import random
from django.db.models import Sum, Avg, Count, Min, Max
from datetime import date

@csrf_exempt
def expenseList(request):
    # check if the request is GET or POST method
    try:
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
                expenses = Expense.objects.all()
                # # print(expenses)
                # expenses = serializers.serialize('json', expenses)
                # return HttpResponse(expenses, content_type='application/json') # safe=False means data is not a dictionary
                return JsonResponse(list(expenses.values()), safe=False)

        elif request.method == 'POST':  # Adding feature to handle bulk data
            data = json.loads(request.body)  # Parse JSON string into a Python object

            print(data)
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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

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
    try:
        if request.method == 'GET':
            query = request.GET.get('title', '') 
            date = request.GET.get('date', '') 
            amount = request.GET.get('amount', '')


            if query or date or amount:
                expenses = Expense.objects.filter(title__icontains=query, amount__icontains=amount, date__icontains=date).values()
            else:
                expenses = Expense.objects.all().values()

            return JsonResponse(list(expenses), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
def expenseUnique(request):
    try:
        if request.method == 'GET':
            target = request.GET.get('target')
            col = ['title', 'amount', 'date']
            if target in col:
                expense = Expense.objects.order_by('-' + target).values(target).distinct()
                return JsonResponse(list(expense), safe=False)
            else:
                return JsonResponse({'message': 'Enter valid target field'})
    except Exception as e: 
        return JsonResponse({'error': str(e)})
    
@csrf_exempt
def expenseRandom(request):
    try:
        if request.method == 'GET':
            # to solve this first get the list of the all the id's present in the database
            allId = Expense.objects.values_list('id', flat=True)
            if not allId:
                return JsonResponse({'error': 'There is nothing present in the DB'})
            # print(allId)
            randId = random.choice(list(allId))
            # print(randId)
            randExpense = Expense.objects.get(id=randId)
            return JsonResponse({'id': randExpense.id, 'title': randExpense.title, 'amount': randExpense.amount, 'date': randExpense.date})
        
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
def _fetchAll():
    expenses = Expense.objects.all().values()
    return JsonResponse(list(expenses), safe=False)

@csrf_exempt
def expenseCustom(request):
    try:
        if request.method == 'GET':
            target = request.GET.get('target')
            if target:
                customCols = Expense.objects.values(target)
                # print(customCols)
                return JsonResponse(list(customCols), safe=False)
            else:
                return _fetchAll()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
def expenseStrictSearch(request):
    try:
        if request.method == 'GET':
            date = request.GET.get('date')
            title = request.GET.get('title')
            amount = request.GET.get('amount')
            
            if date:
                expenses = Expense.objects.filter(date__icontains = date).only('title', 'amount')
                # print(expense)
                expense_list = [{'title': expense.title, 'amount': expense.amount} for expense in expenses]
                return JsonResponse({'expenseList': expense_list})
            elif title:
                expenses = Expense.objects.filter(title__icontains=title).only('amount' ,'date')
                expense_list = [{'amount': expense.amount, 'date': expense.date} for expense in expenses]
                return JsonResponse({'expenseList': expense_list})
            elif amount:
                expenses = Expense.objects.filter(amount__icontains=amount).only('title' ,'date')
                expense_list = [{'title': expense.title, 'date': expense.date} for expense in expenses]
                print(expense_list)
                return JsonResponse(expense_list, safe=False)
            else:
                return _fetchAll()
    except Exception as e:
        return JsonResponse({'error': str(e)}, 400)
    
@csrf_exempt
def expenseSearch(request):
    try:
        if request.method == 'GET':
            title = request.GET.get('title', '')
            amount = request.GET.get('amount', '')
            date = request.GET.get('date', '')
            expense = Expense.objects.filter(title__iexact=title, amount__iexact=amount, date__icontains=date).values()
            return JsonResponse(list(expense), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)})
            
@csrf_exempt
def expenseLatest(request):
    try: 
        if request.method == 'GET':
            target = request.GET.get('target')
            if target in ['id', 'title', 'amount', 'date']:
                expense = Expense.objects.latest(target)
                print(expense)
                return JsonResponse({'id': expense.id, 'title': expense.title, 'amount': expense.amount, 'date': expense.date})
            else:
                return _fetchAll()
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
def expenseCompute(request):
    try: 
        if request.method == 'GET':
            operations = request.GET.getlist('operation')  # Use getlist() to get multiple operations
            
            if operations:
                validOperations = {
                    'count': Count('id'), 
                    'avg': Avg('amount'), 
                    'sum': Sum('amount'), 
                    'min': Min('amount'),
                    'max': Max('amount')
                }

                # Filter only valid operations
                givenOperation = [operation for operation in operations if operation in validOperations]
                
                if givenOperation:
                    kwargsAggregate = {}
                    for operation in givenOperation:
                        kwargsAggregate[operation] = validOperations[operation]

                    # Perform aggregation
                    expense = Expense.objects.aggregate(**kwargsAggregate)
                    
                    return JsonResponse({'message': 'success', 'result': expense})
                else:
                    return JsonResponse({'error': 'Invalid operations provided'}, status=400)
            else:
                return JsonResponse({'error': 'Please, enter any operations'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def expenseDateRange(request):
    try:
        if request.method == 'GET':
            startDate = request.GET.get('start')
            endDate = request.GET.get('end')
            sort = request.GET.get('sort')
            amount = request.GET.get('amount')
            
            # Check if startDate is provided
            if startDate:
                # Handle date range filtering
                if endDate:
                    expenses = Expense.objects.filter(date__range=[startDate, endDate])
                else:
                    # If endDate is not provided, use today's date
                    todayDate = date.today()
                    expenses = Expense.objects.filter(date__range=[startDate, todayDate])
                
                # Handle sorting by date
                if sort in ['asc', 'desc']:
                    if sort == 'asc':
                        expenses = expenses.order_by('date')
                    else:
                        expenses = expenses.order_by('-date')
                
                # Handle filtering by amount (if provided)
                elif amount:
                    try:
                        # Convert amount to an integer
                        amount = float(amount)
                        
                        # Filter expenses where the amount is greater than or equal to the provided value
                        conditionalExpense = sorted(
                            [expense for expense in expenses if expense.amount >= amount],
                            key=lambda x: x.amount
                        )
                        
                        # Return filtered and sorted expenses
                        return JsonResponse(list(expense_to_dict(conditionalExpense)), safe=False)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid amount value'}, status=400)

                # Return expenses sorted by date if no amount filtering is applied
                return JsonResponse(list(expenses.values()), safe=False)
            else:
                return JsonResponse({'error': 'At least start date has to be mentioned'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Helper function to convert model instances to dictionaries if needed
def expense_to_dict(expenses):
    return [{'id': expense.id, 'date': expense.date, 'amount': expense.amount, 'title': expense.title} for expense in expenses]
