from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.expenseList, name='expenseList'),
    path('expense/<pk>', views.expenseDetail, name='expenseDetail'),
    path('expense/search/', views.expenseQuery, name='expenseQuery'),
    path('expense/', views.expenseUnique, name='expenseUnique')
]

