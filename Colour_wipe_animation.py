import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 65     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def clearDisplay(strip, wait_ms=20):
    """Turn off all pixels to clear the display."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)  # Set color to black (off)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print ('Color wipe animations.')
            colorWipe(strip, Color(0, 255, 0))  # Green wipe
            clearDisplay(strip)  # Non-color wipe to turn off all pixels
            colorWipe(strip, Color(255, 0, 0))  # Red wipe
            clearDisplay(strip)  # Non-color wipe to turn off all pixels
            colorWipe(strip, Color(0, 0, 255))  # Blue wipe
            clearDisplay(strip)  # Non-color wipe to turn off all pixels
            colorWipe(strip, Color(0, 255, 0))  # Green wipe
            clearDisplay(strip)  # Non-color wipe to turn off all pixels
            colorWipe(strip, Color(0, 0, 255))  # Blue wipe
            clearDisplay(strip)  # Non-color wipe to turn off all pixels
            time.sleep(5)  # Pause for 5 seconds


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
