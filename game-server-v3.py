import RPi.GPIO as GPIO
import random
import functools
import socket
import threading
import board
import neopixel
from time import sleep
from rpi_ws281x import *
import argparse
import time
import sys
import os
from hubclient import hubclient


huburi = "ws://192.168.0.2:8000/connect" # URI of the EscapeHub WS service
device = { # a dictionary containing our device details
    "room": "1", # ID of the room we are to register to
    "name": "Colour Puzzle", # display name of the device
    "status": "Waiting", # textual status for management display
    "actions": [ # list of actions (of empty list!)
        {
            "actionid": "ACTONE", # the ID we will receive for this action
            "name": "Start Game", # friendly name for display in the hub
            "enabled": True # is this action currently available
        },
        {
            "actionid": "ACTTWO", 
            "name": "Reset Game", 
            "enabled": True 
        },
       
    ]
}

global play_again
global selected_setting_value
global restart_game  # Declare at the top with other global variables
restart_game = False
play_again = input


def ActionHandler(actionid):
    global selected_setting_value
    global restart_game
    global play_again

    print("Action handler for ID " + actionid)
    if actionid == "ACTONE":
        selected_setting_value = "1"
        device['actions'][1]['enabled'] = True
    elif actionid == "ACTTWO":
        play_again = 'yes'
        device['actions'][0]['enabled'] = True
    else:
        print("Unknown action")
    hub.Update(device)

        
hub = hubclient() # the instance of the hubclient

hub.setDebug(True) # will output LOTS to the console

hub.actionHandler = ActionHandler # assign the function above to handle (receive) actions for us

print("Startup")

print("Connecting to EscapeHub via "+huburi)

hub.Connect(huburi)

print("Registering Device")
myid = hub.Register(device)


# If code is stopped during active it will stay active. This may produce a warning if restarted, this line prevents that.
GPIO.setwarnings(False)
# This means we will refer to the GPIO
# by the number after GPIO.
GPIO.setmode(GPIO.BCM)
# This sets up the GPIO 18 pin as an output pin
GPIO.setup(12, GPIO.OUT)
# Turns Relay On. Brings Voltage to Min GPIO can output ~0V. (Sets lock)
GPIO.output(12, 0)

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN2 = board.D18
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 65     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
pixels = neopixel.NeoPixel(LED_PIN2, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)
stop_led_animation = threading.Event()
stop_socket_communication = threading.Event()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = None
# Bind the socket to a specific address and port (replace 'SERVER_IP' and 'SERVER_PORT' with the actual IP and port you want to use)
server_ip = '192.168.0.135'
server_port = 65450
print("Server port working")
server_socket.bind((server_ip, server_port))
print("Socket bind working")

# Listen for incoming connections (1 connection in the queue)
server_socket.listen(1)

# Assigns colour code values to c_code
color_map = {
        1: 'red',
        2: 'green',
        3: 'blue'
    }

c_code = []  # Code that needs to be displayed on the UI as the final sequence is randomly generated using a random function


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=2000):
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

def led_animation(stop_flag):
    try:
        while not stop_flag.is_set():
            for i in range(len(c_code)):
                color = c_code[i][0]  # Get the color number from the code
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
                time.sleep(1)  # Pause for 2 seconds

            time.sleep(5)  # Pause for 5 seconds


    except KeyboardInterrupt:
        # If the animation is interrupted by Ctrl-C, turn off all LEDs
        clearDisplay(strip)
        
def process_event(event):
    if event == 'Exit':
        stop_game = True
        return

    button_number = int(event[-1])
    c_numbers[button_number] += 1
    if c_numbers[button_number] > 3:
        c_numbers[button_number] = 0
    print(f"Processed event: {event}, Button Number: {button_number}")  # Debug line


restart_game = False  # Initialize the global flag

c_numbers = [0, 0, 0, 0, 0]

def socket_communication(stop_flag2):
    # Accept a connection from the client
    print("Waiting for a connection from the client...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    
    global c_numbers
    global stop_game  # Declare stop_game as a global variable
    print(f"Debug c_numbers before using: {c_numbers}")  # Debug line

    while not stop_flag2.is_set():
        received_data = client_socket.recv(1024).decode()
        if not received_data:
            break

        events = received_data.split("Button")[1:]  
        for event in events:
            process_event("Button" + event)

        print("Numbers and Colors:")
        for i, num in enumerate(c_numbers, start=1):
            color = color_map.get(num, 'unknown color')
            print(f"Button {i} ({color}): {num}")

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q[0], c_numbers, c_code), True):
            print("Numbers and code are the same")
            GPIO.output(12, 1)  # This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
            print("GPIO")
            stop_led_animation.set()
            print("Stop LED Animation")
            print("Congratulations! Returning to settings selection...")
            restart_game = True
            return  # Exit the inner loop and go back to selecting setting
        else:
            print("Numbers and code are not the same")

    # Close the client socket
    client_socket.close()

c_numbers = [0, 0, 0, 0, 0]

def test_function():
    global c_numbers
    print(f"Debug c_numbers in test_function: {c_numbers}")

test_function()

def reset_c_numbers():
    global c_numbers
    c_numbers = [0, 0, 0, 0, 0]


def run_socket_communication(stop_flag2):
    t1 = threading.Thread(target=socket_communication, args=(stop_flag2,))
    t1.daemon = True
    t1.start()
    return t1

def run_led_animation(stop_flag):
    t2 = threading.Thread(target=led_animation, args=(stop_flag,))
    t2.daemon = True
    t2.start()
    return t2

# User prompt to select the setting
def selected_setting():
    while True:
        setting = input("Press 1 to start the game: ")
        
        if setting == 'q':
            return None
        elif setting == '1':
            return '1'
        else:
            print("Invalid setting selection. Please choose 1 or 2.")
        

global selected_setting_value
selected_setting_value = "0"

global play_again_value
play_again_value = input

def initialize_leds():
    print("Initializing LEDs...")
    strip.begin()
    print("LED strip initialized.")

def turn_off_leds():
    print("Turning off LEDs...")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def cleanup_leds():
    print("Cleaning up LEDs...")
    GPIO.output(12, 1)
    GPIO.cleanup()
    
def reset_relay():
    GPIO.output(12, 0)


def play_game():
    global client_socket
    global restart_game
    global play_again

    while True: # infinite loop for our device logic
        
        
        
        try:
            print("Starting main try")
            while True:  # Infinite loop to restart the game
                print("Starting main loop")    
                # Generate a new c_code for each game
                for _ in range(5):
                    random_number = random.randint(1, 3)
                    color = color_map[random_number]
                    c_code.append((random_number, color))
                
                restart_game = False  # Reset the restart_game flag at the beginning of each game loop
                
                # Reset threading events
                stop_led_animation.clear()
                stop_socket_communication.clear()
                
                if selected_setting_value == '1':
                    print("Code is", c_code)
                    # Turn off LEDs and initialize them again
                    initialize_leds()

                    try:
                        # Start socket communication and LED animation threads
                        t1 = run_socket_communication(stop_socket_communication)
                        t2 = run_led_animation(stop_led_animation)

                        t1.join()  # Wait for the socket communication thread to complete
                        
                    except KeyboardInterrupt:
                        if restart_game:
                            print("Restarting game...")
                            break  # This will break out of the current game loop and start a new game
                        # Set the stop flag to terminate threads
                        stop_led_animation.set()
                        stop_socket_communication.set()

                        # Wait for threads to complete before cleaning up
                        t1.join()
                        t2.join()
                        
                        turn_off_leds()  # Turn off LEDs
                        cleanup_leds()  # Cleanup LEDs after turning them off
        
                if restart_game:
                    print("Restarting game due to code match...")
                    continue  # Continue to the next iteration of the outer loop
                else:
                    print("Game complete. Do you want to play again?")
                    print("Turning off LEDs...")
                    turn_off_leds()  # Turn off LEDs
                    print("LEDs turned off.")
                    #play_again = input("Enter 'yes' to play again or input 'no' to quit: ")
                    play_again = ""
                    print("Waiting for play again")
                    while play_again == "":
                        sleep(0.05)
                    print("Out of play again while loop")
                    c_code.clear()
                    reset_c_numbers()
                    reset_relay()
                    if play_again.lower() == 'no':
                        # Trigger the "Stop Program" action
                        sys.exit(0)
                        break  # Break out of the outer loop
            else:
                print("Invalid setting selection. Press 'Enter' to play again or input 'no' to quit")
            
            print("Exiting game.")

        finally:
            # Close sockets and cleanup GPIO
            if client_socket:
                client_socket.close()
            server_socket.close()
            GPIO.cleanup()



if __name__ == '__main__':
    try:
        time.sleep(0.05)

        selected_setting_value = "0"
        while selected_setting_value == "0":
            sleep(0.05)
        if selected_setting_value:
            play_game()
        
            
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
    finally:
        print("Cleaning up and quitting.")
        GPIO.cleanup()
