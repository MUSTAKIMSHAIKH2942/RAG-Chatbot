import requests

url = "http://127.0.0.1:5000/chat"
query = {"query": "What is machine learning?"}
response = requests.post(url, json=query)
print(response.json())