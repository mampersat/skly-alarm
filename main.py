import requests

# Check for northen lights
response = requests.get("https://api.auroras.live/v1/?type=all&lat=65.0&long=25.0&forecast=false")

print(response.json())