import requests
import time

import sys
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
        
local_time = "2021-10-10T10:10:10"

def show_checking(position):
    if sys.platform != 'rp2':
        return
    np[position] = (0, 0, 10)
    np.write()

def show_checked(position):
    if sys.platform != 'rp2':
        return
    np[position] = (0, 10, 0)
    np.write()  

def show_alert(position):
    if sys.platform != 'rp2':
        return
    np[position] = (40, 0, 0)
    np.write()

def show_warning(position):
    if sys.platform != 'rp2':
        return
    np[position] = (20, 20, 0)
    np.write()

def get_location():
    # Get location from IP
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
    local_time = response.json()    
    print(f"time: {local_time['datetime']}")
            
    show_checked(0)
    return True

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


def sun():
    # Check for sunrise and sunset
    # Should cache this to 24hrs
    # More interesting if we can check atmospheric conditions like haze and cloud cover, aka "Pretty Sunsets"
    print('Checking for sunrise and sunset')
    show_checking(3)

    try:
        response = requests.get(f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date=today&tzid={tzid}")
        print(request)

        response = requests.get(request)
        sunrise = response.json()['results']['sunrise']
        sunset = response.json()['results']['sunset']

        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")

        sunset_window = 30 # minutes
        if local_time > sunset - sunset_window:
            show_alert(3)
            return
        
        show_checked(3)
    except:
        print('Failed to get sunrise and sunset')
        show_warning(3)

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


def sleep():
    # Pulse light[0] to indicate sleep
    if sys.platform != 'rp2':
        return
    
    for i in range(60):  # sleep 60 seconds
        # Calculate the on_duration using a quadratic function for rapid speed-up
        on_duration = 1.5 - (1.5 / 3600) * (i ** 2)
        off_duration = on_duration / 2  # Adjust off duration to match the speed-up
        
        np[0] = (0, 10, 0)
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

# Main loop

print('Checking for cool things in the sky')

# one time call to get location etc.
get_location()
while True:
    aurora()
    iss()
    sun()
    # meteors()
    # launches()
    # neatclouds()
    # airplanes()

    print('sleeping')
    sleep()