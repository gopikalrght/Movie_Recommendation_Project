import requests

data = {
    "title": "Inception",
    "year": 2010
}

response = requests.post(
    "http://127.0.0.1:5000/watchlist/add",
    json=data
)

print("Status Code:", response.status_code)
print("Response:", response.json())