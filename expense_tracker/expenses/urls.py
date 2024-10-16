from django.urls import path
from . import views

urlpatterns = [
    path('expenses', views.expenseList, name='expenseList'),
    path('expense/<pk>', views.expenseDetail, name='expenseDetail'),
    path('expense/query/', views.expenseQuery, name='expenseQuery'),
    path('expense', views.expenseUnique, name='expenseUnique'),
    path('expense/choice/random', views.expenseRandom, name='expenseRandom'),
    path('expense/choice/custom', views.expenseCustom, name='expenseCustom'),
    path('expense/strict_search/', views.expenseStrictSearch, name='expenseStrictSearch'),
    path('expense/search/', views.expenseSearch, name='expenseSearch'),
    path('expense/latest/', views.expenseLatest, name='expenseLatest'),
    path('expense/compute/', views.expenseCompute, name='expenseCompute'), 
]

