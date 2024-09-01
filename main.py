import requests

# lat/lon of KBTV
lat = 44.4689
lon = -73.1502
tzid = "America/New_York"

def get_location():
    # Get location from IP
    global lat, lon, tzid

    response = requests.get("https://ipinfo.io")
    location = response.json()
    lat = float(location['loc'].split(',')[0])
    lon = float(location['loc'].split(',')[1])
    tzid = location['timezone']
    print(f"{location['city']}, {location['region']} : {location['country']}")

    # get current time
    response = requests.get(f"https://worldtimeapi.org/api/timezone/{tzid}")
    time = response.json()    
    print(f"time: {time['datetime']}")
            
    return True

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
        print('ISS is overhead')
        return True
    
    print('ISS is not overhead')


def sun():
    # Check for sunrise and sunset
    # Should cache this to 24hrs
    # More interesting if we can check atmospheric conditions like haze and cloud cover, aka "Pretty Sunsets"
    request = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date=today&tzid={tzid}"
    print(request)

    response = requests.get(request)
    sunrise = response.json()['results']['sunrise']
    sunset = response.json()['results']['sunset']

    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")

def meteors():
    # Check for meteors
    response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date=2018-10-10&end_date=2018-10-10&api_key=DEMO")


def launches():
    # Check for rocket launches
    response = requests.get("https://launchlibrary.net/1.4/launch/next/5")


def neatclouds():
    # Check for neat cloud formations
    response = requests.get("https://api.nasa.gov/planetary/apod")


def airplanes():
    # Check for airplanes
    response = requests.get("https://opensky-network.org/api/states/all")


def main():
    print('Checking for cool things in the sky')
    get_location()
    aurora()
    iss()
    sun()
    # meteors()
    # launches()
    # neatclouds()
    # airplanes()

if __name__ == '__main__':
    main()
    