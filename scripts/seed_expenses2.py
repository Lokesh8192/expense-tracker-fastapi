import requests

url = "http://127.0.0.1:8000/expenses"

# Replace with your login token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJMb2tpMTIzIiwiZXhwIjoxNzczNTg0MDc1fQ.7aiU5dX95DLBSalPm1CwA-XVKm46UYJ6TEsqw4sl1RE"

headers = {"Authorization": f"Bearer {token}"}

expenses = [
    {"title": "Laptop Cleaning Service", "amount": 600, "category": "Maintenance"},
    {"title": "Parking Fee", "amount": 150, "category": "Transport"},
    {"title": "Tea Snacks", "amount": 90, "category": "Food"},
    {"title": "Printer Ink Cartridge", "amount": 1250, "category": "Office"},
    {"title": "Haircut", "amount": 200, "category": "Personal Care"},
    {"title": "Laundry Service", "amount": 350, "category": "Household"},
    {"title": "Cloud Storage Subscription", "amount": 299, "category": "Software"},
    {"title": "Power Bank Purchase", "amount": 899, "category": "Electronics"},
    {"title": "Notebook Purchase", "amount": 120, "category": "Stationery"},
    {"title": "Temple Donation", "amount": 500, "category": "Charity"},
]
for expense in expenses:
    response = requests.post(url, json=expense, headers=headers)
    print(response.json())
