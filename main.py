import requests

# lat/lon of KBTV
lat = 44.4689
lon = -73.1502

def aurora():
    # Check for northen lights
    # http://auroraslive.io/#/api/v1/all
    response = requests.get(f"https://api.auroras.live/v1/?type=all&lat={lat}&long={lon}&forecast=false&threeday=false")
    pobability = response.json()['probability']['value']

    print(f"Probability of northern lights: {pobability}")
    if pobability > 0.5:
        return True
    
    return False

def iss():
    # Check for ISS
    # http://api.open-notify.org/
    # This API returns the current latitude and longitude of the International Space Station
    # Might need to calculate elevation as it might only be visible shorlty after sunset or before sunrise
    response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_lat = float(response.json()['iss_position']['latitude'])
    iss_lon = float(response.json()['iss_position']['longitude'])
    
    # check if ISS is overhead
    range = 10
    if iss_lat - range < lat < iss_lat + range and iss_lon - range < lon < iss_lon + range:
        return True

def sun():
    # Check for sunrise and sunset
    # Should cache this to 24hrs
    # More interesting if we can check atmospheric conditions like haze and cloud cover
    response = requests.get("https://api.sunrise-sunset.org/json?lat=65.0&lng=25.0&date=today")

def meteors():
    # Check for meteors
    response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date=2018-10-10&end_date=2018-10-10&api_key=DEMO")

def launches():
    # Check for rocket launches
    response = requests.get("https://launchlibrary.net/1.4/launch/next/5")

aurora()
iss()
