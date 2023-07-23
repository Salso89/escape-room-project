import RPi.GPIO as GPIO
import random
import functools
import socket

# If code is stopped during active it will stay active
# This may produce a warning if restarted, this
# line prevents that.
GPIO.setwarnings(False)
# This means we will refer to the GPIO
# by the number after GPIO.
GPIO.setmode(GPIO.BCM)
# This sets up the GPIO 18 pin as an output pin
GPIO.setup(18, GPIO.OUT)
# Turns Relay On. Brings Voltage to Min GPIO can output ~0V. (Sets lock)
GPIO.output(18, 1)

code = [] # Code that needs to be displayed on the UI as the final sequence is randomly generated using a random function
for _ in range(5):
    randomNumber2 = random.randint(0, 9)
    code.append(randomNumber2)
print("Code is", code)

numbers = [0, 0, 0, 0, 0]

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port (replace 'SERVER_IP' and 'SERVER_PORT' with the actual IP and port you want to use)
server_ip = '127.0.0.1'
server_port = 65432
server_socket.bind((server_ip, server_port))

# Listen for incoming connections (1 connection in the queue)
server_socket.listen(1)

# Accept a connection from the client
print("Waiting for a connection from the client...")
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

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

    print("Numbers:", numbers)

    if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
        print("Numbers and code are the same")
        GPIO.output(18, 0)  # This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
        break
    else:
        print("Numbers and code are not the same")

# Close the sockets
client_socket.close()
server_socket.close()
