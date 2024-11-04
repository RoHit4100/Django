from django.db import connection
from ..models import *
from pprint import pprint
from faker import Faker
from django.db.models import Prefetch

def run():
    fake = Faker()
    # print(Restaurant.objects.all().filter(name='EverShine').exists())
    # q = Restaurant.objects.get(id=290)
    # print(q.ratings.all().values()) ## modelName_set will make the reverse connection for the relation

    # pprint(connection.queries)

    # q = Restaurant.objects.filter(date_opened__range=('2024-06-13', '2024-06-30'))
    # pprint(q.values())
    # pprint(connection.queries)


    # select relted and prefetch related 
    # Use prefetch_related to avoid multiple queries for related ratings
    # r = Restaurant.objects.prefetch_related('ratings')

    # # Print each restaurant's ratings
    # for restaurant in r:
    #     pprint(restaurant.ratings.rating)  # Access ratings for each restaurant

    # # Print SQL queries executed
    # pprint(connection.queries)
    
    # restaurants = Restaurant.objects.prefetch_related('ratings', 'sales')
    # print(restaurants)
    
    # # Loop through each restaurant and print details
    # for restaurant in restaurants:
    #     print(f"Restaurant: {restaurant.name}")
    #     print("Ratings:")
        
    #     # Print each rating for the restaurant
    #     for rating in restaurant.ratings.select_related('visited_users'):
    #         print(f" - User: {rating.user.username}, Rating: {rating.rating}, Review: {rating.review}")
        
    #     print("Sales:")
         
    #     # Print each sale for the restaurant
    #     for sale in restaurant.sales.all():
    #         print(f" - Income: {sale.income}, Date: {sale.date_time}")
        
    #     print("\n" + "-"*40 + "\n")  # Separator for readability
    # # pprint(connection.queries)
    
        
    # Original query with optimizations
    # Optimized query without N+1 problem
    restaurants = (
        Restaurant.objects
        .prefetch_related(
            Prefetch(
                'ratings',
                queryset=Rating.objects.select_related('user')
                .only('rating', 'review', 'user__username', 'restaurant_id')
            ),
            Prefetch(
                'sales',
                queryset=Sale.objects.only('income', 'date_time', 'restaurant_id')
            )
        )
        .only(
            'name', 
            'id', 
            'restaurant_type' # Include needed fields from restaurant_type
        )
    )

    print(restaurants)
    # print("\n" + "-"*40 + "\n")
    # Using iterator() for large querysets to reduce memory usage
    # for restaurant in restaurants.iterator(chunk_size=100):
    #     print(f"Restaurant: {restaurant.name}")
    #     print("Ratings:")
        
    #     # No additional queries needed due to prefetch_related
    #     for rating in restaurant.ratings.all():
    #         print(f" - User: {rating.user.username}, Rating: {rating.rating}, Review: {rating.review}")
        
    #     print("Sales:")
        
    #     # No additional queries needed due to prefetch_related
    #     for sale in restaurant.sales.all():
    #         print(f" - Income: {sale.income}, Date: {sale.date_time}")
        
    #     print("\n" + "-"*40 + "\n")


    pprint(connection.queries)