import requests

# lat/lon of KBTV
lat = 44.4689
long = -73.1502

def aurora():
    # Check for northen lights
    # http://auroraslive.io/#/api/v1/all
    response = requests.get(f"https://api.auroras.live/v1/?type=all&lat={lat}&long={long}&forecast=false&threeday=false")
    pobability = response.json()['probability']['value']

    print(f"Probability of northern lights: {pobability}")
    if pobability > 0.5:
        return True

def iss():
    # Check for ISS
    response = requests.get("http://api.open-notify.org/iss-now.json")

def sun():
    # Check for sunrise and sunset
    response = requests.get("https://api.sunrise-sunset.org/json?lat=65.0&lng=25.0&date=today")

def meteors():
    # Check for meteors
    response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date=2018-10-10&end_date=2018-10-10&api_key=DEMO")

def launches():
    # Check for rocket launches
    response = requests.get("https://launchlibrary.net/1.4/launch/next/5")

aurora()
