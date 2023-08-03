import board
import neopixel
from time import sleep
import random
import functools
import socket
import threading
import RPi.GPIO as GPIO

# Constants
LED_COUNT = 150
LED_PIN = board.D18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 65
LED_INVERT = False
LED_CHANNEL = 0

# If code is stopped during active, it will stay active
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

# Assigns morse code values
morseCode = {
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----'
}

code = []

# Generates random code for 'code' list
code = []
for _ in range(5):
    randomNumber2 = random.randint(0, 9)
    code.append(randomNumber2)
print("Code is", code)

numbers = [0, 0, 0, 0, 0]

# Converts 'code' list to a string
codeString = ''.join(str(num) for num in code)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binds the socket to a specific address and port
server_ip = '127.0.0.1'
server_port = 65436
server_socket.bind((server_ip, server_port))

# Listens for incoming connections (1 connection in the queue)
server_socket.listen(1)

# Accepts a connection from the client
print("Waiting for a connection from the client...")
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Create a neopixel object
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

# Function to send message to LED strip
def sendMorseCode(message):
    for char in message:
        if char in morseCode:
            newCode = morseCode[char]
            for symbol in newCode:
                if symbol == '.':
                    pixels.fill((255, 0, 0))  # Red color for dot
                    pixels.show()  # Update the LED strip
                    sleep(0.2)  # This is the duration of the dot
                elif symbol == '-':
                    pixels.fill((0, 255, 0))  # Green color for dash
                    pixels.show()  # Update the LED strip
                    sleep(1)  # This is the duration of the dash
                pixels.fill((0, 0, 0))  # Turn off the LED after symbol
                pixels.show()  # Update the LED strip
                sleep(0.2)  # This will represent the gap between the code symbols
            sleep(2)  # This will represent the gap between the characters
        else:
            # Ignore non-morse code characters
            continue
    
    sleep(5)  # Pause at the end of the message

# Function for the LED animation
def led_animation(stop_flag):
    try:
        while not stop_flag.is_set():
            sendMorseCode(codeString)
    except KeyboardInterrupt:
        # If the animation is interrupted by Ctrl-C, turn off all LEDs
        pixels.fill((0, 0, 0))
        pixels.show()
        

# Function for socket communication
def socket_communication():
    while True:
        event = client_socket.recv(1024).decode()
        if not event:
            break

        if event == 'Exit':
            break

        button_number = int(event[-1])
        numbers[button_number] += 1
        if numbers[button_number] > 9:
            numbers[button_number] = 0

        print("Button Press Counts:")
        for i, num in enumerate(numbers, start=1):
            print(f"Button {i}: {num}")

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
            print("Numbers and code are the same")
            GPIO.output(12, 0)  # This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
            stop_led_animation.set()
            break
        else:
            print("Numbers and code are not the same")

    # Close the client socket
    client_socket.close()

if __name__ == '__main__':
    stop_led_animation = threading.Event()

    # Start socket communication in a separate thread
    t1 = threading.Thread(target=socket_communication)
    t1.start()

    # Start LED animation in a separate thread
    t2 = threading.Thread(target=led_animation, args=(stop_led_animation,))
    t2.start()

    try:
        while True:
            sleep(1)  # Keep the main thread alive

    except KeyboardInterrupt:
        # If the program is interrupted by Ctrl-C, clean up GPIO and stop the LED animation
        stop_led_animation.set()
        pixels.fill((0, 0, 0))
        pixels.show()
        GPIO.output(12, 0)  # This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
        GPIO.cleanup()
