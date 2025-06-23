import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer not-needed"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant that explains Python concepts."},
        {"role": "user", "content": "How do I write a for loop in Python?"}
    ],
    "temperature": 0.7
}

response = requests.post("http://localhost:1234/v1/chat/completions", headers=headers, json=data)
print(response.json())
