import requests
import json

api_url = "https://api.jikan.moe/v4/anime?page=1"
response = requests.get(api_url)

print(len(response.json()["data"]))
with open("data2.json", "w") as f:
    json.dump(response.json(), f, indent=4)