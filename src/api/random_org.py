import requests

from src.util import config


def generate_string():
    payload = {
        "jsonrpc": "2.0",
        "method": "generateStrings",
        "params": {
            "apiKey": config.RND_API_KEY,
            "n": 1,  # Number of random strings to generate
            "length": 10,  # Length of each string
            "characters": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Characters to use
        },
        "id": 42
    }

    response = requests.post(config.RND_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        random_string = result['result']['random']['data'][0]
        return random_string
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
