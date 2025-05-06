import requests

# API endpoint and key
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
api_key = "AIzaSyA5Uy_ty3R0y3sjHluc3pdEGsuggT8EUeY"

# Request payload
payload = {
    "contents": [
        {
            "parts": [{"text": "What is coding?"}],
        }
    ]
}

# Headers
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)

# Handle the response
if response.status_code == 200:
    result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    cleaned_result = result.replace("**", "").strip()
    print(cleaned_result)
else:
    print(f"Error: {response.status_code}, {response.text}")