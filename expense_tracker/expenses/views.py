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
            # Retrieve query parameters
            operation = request.GET.get('sort', 'asc')  # Default to 'asc' if not provided
            target = request.GET.get('on', 'id')  # Default sort field if 'on' is not provided

            # map target to model fields and build query
            order_prefix = '' if operation == 'asc' else '-'
            order_field = f"{order_prefix}{target}" if target in {'date', 'amount', 'title'} else 'id'
            expenses = Expense.objects.order_by(order_field).values('id', 'title', 'amount', 'date')
            
            return JsonResponse(list(expenses), safe=False)
        else:
            return JsonResponse({'error':'only GET method is allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)


def saveBatch(batchData):
    # with keyword uswe to create context manager(way to allocate and release the resources when I want)
    with transaction.atomic(): # all operations are either commited or nothing in the batch, rollback if exception is raised
        Expense.objects.bulk_create(batchData)

@csrf_exempt 
def addExpenses(request):
    try:
        if request.method == 'POST':
            # check if the data is instance of the list or not
            data = json.loads(request.body)
            
            if isinstance(data, list): # this will check if the current data is list or not
                expenseBatch = [
                    Expense(title=item.get('title'), amount=item.get('amount'), date=item.get('date'))
                    for item in data if item.get('title') and item.get('amount') and item.get('date')
                ]

                
                if not expenseBatch:
                    return JsonResponse({'error': 'Invalid data in batch'}, status=400)
                
                # using threading pool to handle batch saving concurrently
                with ThreadPoolExecutor(max_workers=5) as executor:
                    # now process the data while using batch
                    for i in range(0, len(expenseBatch), 100):
                        batch = expenseBatch[i:i + 100]
                        executor.submit(saveBatch, batch)
                
                return JsonResponse({'message': 'Expenses are added successfully'}, status=200)
            # handle single data entry
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
        else:
            return JsonResponse({'error': 'only POST method is allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = 400)



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
                if performOperations(operations):
                    kwargsAggregate = performOperations(operations)
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
            
            # Check if startDate exists or not
            if startDate:
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
                        # As conditionalExpense is present in the form of list of objects, convert this list into
                        # list of objects, which will hold the information
                        return JsonResponse(list(expense_to_dict(conditionalExpense)), safe=False)
                    except Exception as e:
                        return JsonResponse({'error': str(e)}, status=400)

                # Return expenses sorted by date if no amount filtering is applied
                return JsonResponse(list(expenses.values()), safe=False)
            else:
                return JsonResponse({'error': 'At least start date has to be mentioned'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def expense_to_dict(expenses):
    return [{'id': expense.id, 'title': expense.title, 'date': expense.date, 'amount': expense.amount} for expense in expenses]

def performOperations(givenOperations):
    validOperations = {
        'count': Count('id'), 
        'avg': Avg('amount'), 
        'sum': Sum('amount'), 
        'min': Min('amount'),
        'max': Max('amount')
    }
    # now traverse for each operation in operations, and get the valid operations
    operations = [operation for operation in givenOperations if operation in ['count', 'avg', 'sum', 'min', 'max']]
    # now create kwargs to pass in the aggregate function
    if operations:
        kwargsForAggregate = {}
        for operation in operations:
            kwargsForAggregate[operation] = validOperations[operation]
        
        return kwargsForAggregate
    else : return None

@csrf_exempt
def expenseForDate(request):
    try:
        if request.method == 'GET':
            # get the date 
            targetDate = request.GET.get('date')
            operationString = request.GET.get('operations')
            if targetDate:
                expenses =  Expense.objects.filter(date__iexact=targetDate)
                if operationString:
                    # split the operations from ,
                    givenOperations = operationString.split(',')
                    # perform the given operations
                    if givenOperations:
                        if performOperations(givenOperations):
                            kwargsForAggregate = performOperations(givenOperations)
                            
                            afterComputation = expenses.aggregate(**kwargsForAggregate)
                            return JsonResponse({'message': 'success', 'answer': afterComputation})
                        else:
                            return JsonResponse({'error': 'operations are not valid'}, status=400)
                    else:
                        return JsonResponse({'error': 'operations are not valid'}, status=400)
                else:        
                    return JsonResponse(list(expenses.values()), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, 400)
    
@csrf_exempt
def expensesForMonths(request):
    try:
        if request.method == "GET":
            # Get the parameters
            givenYear = request.GET.get('year')
            givenMonth = request.GET.get('month')
            operations = request.GET.get('operations')
            sort = request.GET.get('sort')
            target = request.GET.get('target')

            # Default query to current month if no date parameters are provided
            if not givenMonth and not givenYear:
                currentMonth = date.today().month
                currentYear = date.today().year
                expenses = Expense.objects.filter(date__year=currentYear, date__month=currentMonth)
            elif givenMonth and givenYear:
                # Filter by the given month and year
                givenMonth = int(givenMonth)
                givenYear = int(givenYear)
                expenses = Expense.objects.filter(date__year=givenYear, date__month=givenMonth)
            else:
                return JsonResponse({'message': 'Please enter valid parameters'}, status=400)

            # Apply operations if provided
            if operations:
                givenOperations = operations.split(',')
                kwargsAggregate = performOperations(givenOperations)
                if kwargsAggregate:
                    result = expenses.aggregate(**kwargsAggregate)
                    return JsonResponse({'message': 'success', 'result': result})
                else:
                    return JsonResponse({'error': 'Invalid operations provided'}, status=400)

            # Apply sorting logic
            if sort and target:
                if sort == 'asc':
                    if target in ['id', 'title', 'amount', 'date']:
                        expenses = expenses.order_by(target)
                elif sort == 'desc':
                    if target in ['id', 'title', 'amount', 'date']:
                        expenses = expenses.order_by(f'-{target}')
                else:
                    return JsonResponse({'error': 'Invalid sort order'}, status=400)
            elif sort and not target:  # Sorting without target defaults to 'id'
                if sort == 'asc':
                    expenses = expenses.order_by('id')
                elif sort == 'desc':
                    expenses = expenses.order_by('-id')
                else:
                    return JsonResponse({'error': 'Invalid sort order'}, status=400)

            # Return the queryset as JSON
            return JsonResponse(list(expenses.values('id', 'title', 'amount', 'date')), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


