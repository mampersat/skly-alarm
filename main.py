import requests

# Check for northen lights
response = requests.get("https://api.auroras.live/v1/?type=all&lat=65.0&long=25.0&forecast=false")

# Check for ISS
response = requests.get("http://api.open-notify.org/iss-now.json")

# Check for sunrise and sunset
response = requests.get("https://api.sunrise-sunset.org/json?lat=65.0&lng=25.0&date=today")

# Check for meteors
response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date=2018-10-10&end_date=2018-10-10&api_key=DEMO")

# Check for rocket launches
response = requests.get("https://launchlibrary.net/1.4/launch/next/5")


