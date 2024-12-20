import json
import requests
import random
from datetime import datetime, timedelta

# URL of your Django API endpoint
url = 'http://127.0.0.1:8000/api/expenses'
exp = [
    "Grocery Shopping", 
    "Utility Bills", 
    "Rent Payment", 
    "Transportation Costs", 
    "Dining Out", 
    "Gym Membership", 
    "Internet Subscription", 
    "Mobile Phone Bill", 
    "Insurance Premium", 
    "Entertainment (Movies/Streaming)", 
    "Fuel Expense", 
    "Medical Bills", 
    "Clothing Purchase", 
    "Car Maintenance", 
    "Home Repairs", 
    "Subscriptions (Magazines/Apps)", 
    "Parking Fees", 
    "Loan Repayment", 
    "Childcare Expenses", 
    "Household Supplies", 
    "Vacation Fund", 
    "Pet Care", 
    "Credit Card Payment", 
    "Charitable Donations", 
    "Education Fees", 
    "Self-care Products", 
    "Gifts and Celebrations", 
    "Furniture Purchase", 
    "Work-related Expenses", 
    "Laundry and Dry Cleaning"
]

# Function to generate random dummy expense data
def generate_dummy_data(count):
    expenses = []
    start_date = datetime.today()
    for i in range(count):
        expenses.append({
            "title": f"{random.choice(exp)}",
            "amount": round(random.uniform(10, 1000), 2),
            "date": (start_date - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        })
    return expenses

# Generate 10,000 dummy expenses
dummy_data = generate_dummy_data(10000)

# Send POST request in batches to avoid large payload issues
batch_size = 1000  # Posting 1000 records at a time

for i in range(0, len(dummy_data), batch_size):
    batch = dummy_data[i:i + batch_size]
    response = requests.post(url, json=batch)
    

