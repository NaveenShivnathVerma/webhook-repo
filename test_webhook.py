# test_webhook.py
import requests
import json

url = "http://localhost:5000/webhook/receiver"

headers = {
    "Content-Type": "application/json",
    "X-GitHub-Event": "push"
}

data = {
    "pusher": {
        "name": "Travis"
    },
    "ref": "refs/heads/main"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print("Status Code:", response.status_code)
print("Response:", response.json())
