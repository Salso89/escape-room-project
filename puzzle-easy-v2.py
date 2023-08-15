import PySimpleGUI as sg
import socket
import random

sg.theme('DarkAmber')

numbers = [0,0,0,0,0] # Numbers that are initially displayed on the UI are randomly generated using a random function


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (replace 'SERVER_IP' and 'SERVER_PORT' with the actual IP and port of the server)
server_ip = '192.168.0.135'
server_port = 65450
client_socket.connect((server_ip, server_port))

# Layout of the UI is established using a series of container objects called frames that have been called using the PySimpleGUI import
layout = [[sg.Frame('', layout=[], size=(1, 10))], [sg.T('   Enter Code below ... ', font=('Krungthep', 30), pad=(0, 30))],

[
    sg.Frame('', element_justification='center', layout=[[sg.T(numbers[0], font=("Krungthep", 90), key='Number0', pad=(
        10, 10))], [sg.Button('PRESS', key="Button0", font=('Kohinoor Telugu', 17), size=(5,2))]]),
    sg.Frame('', element_justification='center', layout=[[sg.T(numbers[1], font=("Krungthep", 90), key='Number1', pad=(
        10, 10))], [sg.Button('PRESS', key="Button1", font=('Kohinoor Telugu', 17), size=(5,2))]]),
    sg.Frame('', element_justification ='center', layout=[[sg.T(numbers[2], font=("Krungthep", 90), key='Number2', pad=(
        10, 10))], [sg.Button('PRESS', key="Button2", font=('Kohinoor Telugu', 17), size=(5,2))]]),
    sg.Frame('', element_justification='center', layout=[[sg.T(numbers[3], font=("Krungthep", 90), key='Number3', pad=(
        10, 10))], [sg.Button('PRESS', key="Button3", font=('Kohinoor Telugu', 17), size=(5,2))]]),
    sg.Frame('', element_justification='center', layout=[[sg.T(numbers[4], font=("Krungthep", 90), key='Number4', pad=(
        10, 10))], [sg.Button('PRESS', key="Button4", font=('Kohinoor Telugu', 17), size=(5,2))]])
],

]

window = sg.Window("Key Pad", layout, size=(680, 520), element_justification='center', finalize=True)
window.Maximize()

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    elif event.startswith('Button0'):
        numbers[0] += 1
        if numbers[0] > 3:
            numbers[0] = 0
      
        window['Number0'].update(numbers[0])
        # Send the button press event to the server
        client_socket.send(event.encode())

    elif event.startswith('Button1'):
        numbers[1] += 1
        if numbers[1] > 3:
            numbers[1] = 0

        window['Number1'].update(numbers[1])
        # Send the button press event to the server
        client_socket.send(event.encode())

    elif event.startswith('Button2'):
        numbers[2] += 1
        if numbers[2] > 3:
            numbers[2] = 0

        window['Number2'].update(numbers[2])
        # Send the button press event to the server
        client_socket.send(event.encode())
        
    elif event.startswith('Button3'):
        numbers[3] += 1
        if numbers[3] > 3:
            numbers[3] = 0

        window['Number3'].update(numbers[3])
        # Send the button press event to the server
        client_socket.send(event.encode())

    elif event.startswith('Button4'):
        numbers[4] += 1
        if numbers[4] > 3:
            numbers[4] = 0

        window['Number4'].update(numbers[4])
        # Send the button press event to the server
        client_socket.send(event.encode())

window.close()
