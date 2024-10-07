import requests
import time

import sys

# Useful for running locally vs. on device
if sys.platform == 'rp2':
    import wifi
    from lights import np # TODO maybe remove - this doesn't really do much
else:
    np = [None] * 10

# Location and time information
# Get's overwritten by get_location()
lat = 44.4689
lon = -73.1502
tzid = "America/New_York"
local_time = "2024-08-30T10:10:10" # overwirrten by get_location()
dark = False # overwritten by darkness()

def start_up_animation():
    if sys.platform != 'rp2':
        return

    # Start up animation
    for i in range(10):
        np[i] = (10, 0, 0) # red
        np.write()
        time.sleep(0.1)

    for i in range(10):
        np[i] = (0, 10, 0) # green
        np.write()
        time.sleep(0.1)

    for i in range(10):
        np[i] = (0, 0, 10) # blue
        np.write()
        time.sleep(0.1)

    for i in range(10):
        np[i] = (0, 0, 0) # off
        np.write()
        time.sleep(0.1)


def show_checking(position):
    if sys.platform != 'rp2':
        return
    np[position] = (0, 0, 10) # blue
    np.write()

def show_checked(position):
    if sys.platform != 'rp2':
        return
    np[position] = (0, 10, 0) # green
    np.write()  


def show_alert(position):
    if sys.platform != 'rp2':
        return
    np[position] = (40, 0, 0) # red
    np.write()

def show_warning(position):
    if sys.platform != 'rp2':
        return
    np[position] = (20, 20, 0)
    np.write()

def get_location():
    # Get location from IP
    print("Asking ipinfo.io for approx. location information")

    global lat, lon, tzid, local_time
    show_checking(0)

    response = requests.get("https://ipinfo.io")
    location = response.json()
    lat = float(location['loc'].split(',')[0])
    lon = float(location['loc'].split(',')[1])
    tzid = location['timezone']
    print(f"{location['city']}, {location['region']} : {location['country']}")

    # get current time
    response = requests.get(f"https://worldtimeapi.org/api/timezone/{tzid}")
    local_time = response.json()['datetime']
    print(f"time: {local_time}")
            
    show_checked(0)
    return True

def sky_cover():
    # Check for cloud cover
    # https://api.weather.gov/points/44.4689,-73.1502
    response = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
    forecast = response.json()['properties']['forecast']
    sky_cover = forecast['properties']['skyCover']


def aurora():
    # Check for northen lights
    print('Checking for aurora')
    show_checking(1)

    try:
        response = requests.get(f"https://api.auroras.live/v1/?type=all&lat={lat}&long={lon}&forecast=false&threeday=false")    
    except: 
        print('Failed to get aurora data')
        show_warning(1)
        return
    
    pobability = response.json()['probability']['value']

    print(f"Probability of northern lights: {pobability}")
    if pobability > 0.5:
        show_alert(1)
        return True

    show_checked(1)    
    return False

def iss():
    # Check for ISS
    # http://api.open-notify.org/
    # This API returns the current latitude and longitude of the International Space Station
    # Might need to calculate elevation as it might only be visible shorlty after sunset or before sunrise
    
    print('Checking for ISS')
    show_checking(2)

    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")
    except:
        print('Failed to get ISS location')
        show_warning(2)
        return

    iss_lat = float(response.json()['iss_position']['latitude'])
    iss_lon = float(response.json()['iss_position']['longitude'])

    # check if ISS is overhead
    range = 10
    if iss_lat - range < lat < iss_lat + range and iss_lon - range < lon < iss_lon + range:
        show_alert(2)
        return True
    
    show_checked(2)
    print('ISS is not overhead')
    return False


def meteors():
    # Check for meteors
    response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date=2018-10-10&end_date=2018-10-10&api_key=DEMO")


def launches():
    # Check for rocket launches in the next 12 hours

    print('Checking for rocket launches')

    ## dev API
    response = requests.get("https://lldev.thespacedevs.com/2.2.0/launch/upcoming/")

    # production API
    # response = requests.get("https://ll.thespacedevs.com/2.2.0/launch/upcoming/")

    for result in response.json()['results']:
        window_start = result['window_start']
        # check if in next 12 hours
        if local_time < window_start and local_time > window_start - 12:
            print(result['name'])
            show_alert(4)
            return



def neatclouds():
    # Check for neat cloud formations
    response = requests.get("https://api.nasa.gov/planetary/apod")


def airplanes():
    # Check for airplanes
    response = requests.get("https://opensky-network.org/api/states/all")


def sleep():
    # Pulse light[0] to indicate sleep
    if sys.platform != 'rp2':
        return
    
    for i in range(60):  # sleep 60 seconds
        # Calculate the on_duration using a quadratic function for rapid speed-up
        on_duration = 1.5 - (1.5 / 3600) * (i ** 2)
        off_duration = on_duration / 2  # Adjust off duration to match the speed-up
        
        if dark:
            np[0] = (0, 10, 0) # green
        else:
            np[0] = (10, 10, 0) # yellow

        np.write()
        time.sleep(on_duration)
        
        # Turn off the light
        np[0] = (0, 0, 0)
        np.write()
        time.sleep(off_duration)

    # Excploding pulse from 10 to 0
    for i in range(10, 0, -1):
        np[0] = (40 * i, 0, 0)
        np.write()
        time.sleep(0.1)

    np[0] = (0, 10, 0)
    np.write()

def darkness():
    # determine phase of light, i.e. twilight, nighttime, daytime
    # https://sunrise-sunset.org/api

    global dark

    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date=today&formatted=0"
    print(f"Getting darkness information from {url}")
    response = requests.get(url)

    astronnomical_twilight_begin = response.json()['results']['astronomical_twilight_begin']
    astronnomical_twilight_end = response.json()['results']['astronomical_twilight_begin']

    
    # use the returned TIMES from the API call and today's date to do range checks
    # TODO - date arithmetic, always fun
    is_sun_up = response.json()['results']['sunrise'] < local_time < response.json()['results']['sunset']
    are_we_in_astronimical_night = response.json()['results']['astronomical_twilight_begin'] < local_time < response.json()['results']['astronomical_twilight_end']
    print(f"Local time: {local_time}")
    print(f"Astonomical twilight begin: {response.json()['results']['astronomical_twilight_begin']}")
    print(f"Astonomical twilight end: {response.json()['results']['astronomical_twilight_end']}")
    print(f"Astronomical night: {are_we_in_astronimical_night}")

    print(f"Sun is up: {is_sun_up}")
    
    dark = are_we_in_astronimical_night

    print(response.json())
    return response.json()['results']

if sys.platform == 'rp2':
    print('Running on RP2040')

    print('Checking for cool things in the sky')

    start_up_animation()

    # one time call to get location etc.
    get_location()

    while True:
        # todo: check for new location every 24 hours
        # visibility()
        darkness()
        aurora()
        iss()
        # meteors()
        # launches()
        # neatclouds()
        # airplanes()

        print('sleeping')
        sleep()