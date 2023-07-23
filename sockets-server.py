import PySimpleGUI as sg
import socket

# IP address and port of the first Raspberry Pi
SERVER_IP = '127.0.0.1'  # Replace with the actual IP address
SERVER_PORT = 8888  # Replace with the actual port number

# Create a socket for communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (first Raspberry Pi)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Set up the PySimpleGUI interface
sg.theme('DarkAmber')

layout = [
    [sg.Text('Enter the code:', font=('Helvetica', 16))],
    [sg.Input(size=(10, 1), key='-CODE-', font=('Helvetica', 16))],
    [sg.Button('Submit', key='-SUBMIT-', font=('Helvetica', 16))]
]

window = sg.Window('Lock Control', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == '-SUBMIT-':
        code = values['-CODE-']

        # Send the code to the server (first Raspberry Pi)
        client_socket.send(code.encode())

        # Receive the verification result from the server
        verification_result = client_socket.recv(1024).decode()

        if verification_result == 'CORRECT':
            sg.popup('Code is correct. Lock opened.')
        else:
            sg.popup('Code is incorrect.')

window.close()
