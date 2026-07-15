import urllib.request
import json

api_key = "AIzaSyD8h0tHaoRhQAdQcz4ays7sF49Q--XmtX8"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        for model in data.get('models', []):
            print(model['name'])
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
