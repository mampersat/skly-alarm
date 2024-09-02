# Update the SSID and password in the script below and rename to wifi.py

import network
import time

time.sleep(1)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('<SSID>', '<password>')

print('wifi connected')
