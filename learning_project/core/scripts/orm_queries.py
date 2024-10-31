from django.db import connection
from ..models import *
from pprint import pprint
from faker import Faker

def run():
    fake = Faker()
    # print(Restaurant.objects.all().filter(name='EverShine').exists())
    q = Restaurant.objects.get(id=290)
    print(q.sales.all().values()) ## modelName_set will make the reverse connection for the relation

    # pprint(connection.queries)

