import machine
import neopixel

# It's useful to test a longer strip periodically, so just init to 100
# lights = max(airport_pixel.values()) +1
lights = 10

neopixel_pin = 28
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), lights)