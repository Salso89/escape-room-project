import RPi.GPIO as GPIO
import random
import functools
import socket
import time
from rpi_ws281x import *
import argparse
import threading

# If code is stopped during active it will stay active
# This may produce a warning if restarted, this
# line prevents that.
GPIO.setwarnings(False)
# This means we will refer to the GPIO
# by the number after GPIO.
GPIO.setmode(GPIO.BCM)
# This sets up the GPIO 18 pin as an output pin
GPIO.setup(12, GPIO.OUT)
# Turns Relay On. Brings Voltage to Min GPIO can output ~0V. (Sets lock)
GPIO.output(12, 1)

color_map = {
    1: 'red',
    2: 'green',
    3: 'blue'
}

code = [] # Code that needs to be displayed on the UI as the final sequence is randomly generated using a random function

for _ in range(5):
    random_number = random.randint(1, 3)
    color = color_map[random_number]
    code.append((random_number, color))

print("Code is", code)

numbers = [0, 0, 0, 0, 0]

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port (replace 'SERVER_IP' and 'SERVER_PORT' with the actual IP and port you want to use)
server_ip = '127.0.0.1'
server_port = 65438
server_socket.bind((server_ip, server_port))

# Listen for incoming connections (1 connection in the queue)
server_socket.listen(1)

# Accept a connection from the client
print("Waiting for a connection from the client...")
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

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
def colorWipe(strip, color, wait_ms=5):
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

def led_animation():
    try:
        while True:
            for i in range(len(code)):
                color = code[i][0]  # Get the color number from the code
                rgb_color = Color(0, 0, 0)  # Initialize the color as black (off)

                # Map the color number to the corresponding RGB value
                if color == 1:
                    rgb_color = Color(255, 0, 0)  # Red
                elif color == 2:
                    rgb_color = Color(0, 255, 0)  # Green
                elif color == 3:
                    rgb_color = Color(0, 0, 255)  # Blue

                # Display the color on the LED strip for 1 second
                colorWipe(strip, rgb_color, wait_ms=20)

                # Turn off all LEDs for 500ms between colors
                clearDisplay(strip, wait_ms=20)            
            
            time.sleep(5)  # Pause for 5 seconds


    except KeyboardInterrupt:
        # If the animation is interrupted by Ctrl-C, turn off all LEDs
        clearDisplay(strip)

def socket_communication():
    while True:
        event = client_socket.recv(1024).decode()
        if not event:
            break

        if event == 'Exit':
            break

        button_number = int(event[-1])
        numbers[button_number] += 1
        if numbers[button_number] > 3:
            numbers[button_number] = 0

        print("Numbers and Colors:")
        for i, num in enumerate(numbers, start=1):
            color = color_map.get(num, 'unknown color')
            print(f"Button {i} ({color}): {num}")

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q[0], numbers, code), True):
            print("Numbers and code are the same")
            GPIO.output(12, 0)  # This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
            break
        else:
            print("Numbers and code are not the same")

    # Close the client socket
    client_socket.close()

def run_socket_communication():
    t1 = threading.Thread(target=socket_communication)
    t1.start()

def run_led_animation():
    t2 = threading.Thread(target=led_animation)
    t2.start()

if __name__ == '__main__':
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

    run_socket_communication()
    run_led_animation()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)

    finally:
        # Close the sockets and cleanup GPIO
        client_socket.close()
        server_socket.close()
        GPIO.cleanup()
