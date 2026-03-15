import requests

url = "http://127.0.0.1:8000/expenses"

# Replace with your login token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJMb2tlc2gyMzQiLCJleHAiOjE3NzM1MTA1MjR9.wzSNloTeDEKh-RL4QMRPiQaksbmJsjrS8PZEaN0JVmw"

headers = {"Authorization": f"Bearer {token}"}

expenses = [
    {"title": "Coffee", "amount": 120, "category": "Food"},
    {"title": "Petrol", "amount": 1800, "category": "Fuel"},
    {"title": "Movie Tickets", "amount": 450, "category": "Entertainment"},
    {"title": "Gym Membership", "amount": 1500, "category": "Health"},
    {"title": "Electricity Bill", "amount": 2200, "category": "Utilities"},
    {"title": "Online Course", "amount": 3500, "category": "Education"},
    {"title": "Lunch", "amount": 250, "category": "Food"},
    {"title": "Cab Ride", "amount": 320, "category": "Transport"},
    {"title": "Phone Recharge", "amount": 699, "category": "Utilities"},
    {"title": "Stationery", "amount": 180, "category": "Office"},
]

for expense in expenses:
    response = requests.post(url, json=expense, headers=headers)
    print(response.json())
