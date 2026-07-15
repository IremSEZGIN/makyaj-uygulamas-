import urllib.request
import json

api_key = "AIzaSyD8h0tHaoRhQAdQcz4ays7sF49Q--XmtX8"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

data = {
    "contents": [{"parts": [{"text": "Hello"}]}]
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
