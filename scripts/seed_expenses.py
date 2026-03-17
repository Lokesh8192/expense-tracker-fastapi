import requests

url = "http://127.0.0.1:8000/expenses"

# Replace with your login token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJMb2tpMTIzIiwiZXhwIjoxNzczNzU2NDQxfQ.Fc99CYcVsEim5gD3w1yNOOU-F3IzB_3pMqHt3RVkyWE"

headers = {"Authorization": f"Bearer {token}"}

expenses = [
    {"title": "Lunch at Restaurant", "amount": 250, "category": "Food"},
    {"title": "Breakfast Cafe", "amount": 180, "category": "Food"},
    {"title": "Dinner with Friends", "amount": 750, "category": "Food"},
    {"title": "Supermarket Groceries", "amount": 1800, "category": "Groceries"},
    {"title": "Vegetable Market", "amount": 320, "category": "Groceries"},
    {"title": "Milk and Bread", "amount": 120, "category": "Groceries"},
    {"title": "Bike Petrol", "amount": 500, "category": "Transport"},
    {"title": "Uber Ride", "amount": 240, "category": "Transport"},
    {"title": "Bus Pass", "amount": 600, "category": "Transport"},
    {"title": "Amazon Headphones", "amount": 1999, "category": "Shopping"},
    {"title": "New Shoes", "amount": 3200, "category": "Shopping"},
    {"title": "Phone Case", "amount": 399, "category": "Shopping"},
    {"title": "Electricity Bill", "amount": 1450, "category": "Utilities"},
    {"title": "Water Bill", "amount": 350, "category": "Utilities"},
    {"title": "Internet Bill", "amount": 899, "category": "Utilities"},
    {"title": "Movie Ticket", "amount": 300, "category": "Entertainment"},
    {"title": "Netflix Subscription", "amount": 649, "category": "Entertainment"},
    {"title": "Concert Ticket", "amount": 2500, "category": "Entertainment"},
    {"title": "Gym Membership", "amount": 1200, "category": "Health"},
    {"title": "Protein Powder", "amount": 2400, "category": "Health"},
    {"title": "Doctor Consultation", "amount": 700, "category": "Health"},
    {"title": "Flight Ticket", "amount": 7500, "category": "Travel"},
    {"title": "Hotel Booking", "amount": 5200, "category": "Travel"},
    {"title": "Taxi Airport", "amount": 650, "category": "Travel"},
    {"title": "Online Course", "amount": 1999, "category": "Education"},
    {"title": "Books Purchase", "amount": 850, "category": "Education"},
    {"title": "Exam Fee", "amount": 1200, "category": "Education"},
    {"title": "Mobile Recharge", "amount": 399, "category": "Bills"},
    {"title": "Credit Card Bill", "amount": 4200, "category": "Bills"},
    {"title": "Insurance Premium", "amount": 3100, "category": "Bills"},
]

for expense in expenses:
    response = requests.post(url, json=expense, headers=headers)
    print(response.json())
