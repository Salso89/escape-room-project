import PySimpleGUI as sg
import random
import functools
from tkinter import *
import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep
import threading


#Assigning LED to board number (BCM)
led = LED(23)

#Assign morse code values
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

#If code is stopped during active it will stay active, this may produce a warning if restarted, this line prevents that.
GPIO.setwarnings(False)
#This means we will refer to the GPIO by the number after GPIO.
GPIO.setmode(GPIO.BCM)
#This sets up the GPIO 18 pin as an output pin
GPIO.setup(18, GPIO.OUT)
#Turns Relay On. Brings Voltage to Min GPIO can output ~0V. (Sets lock)
GPIO.output(18, 1)

#sets colour scheme for pysimplegui interface
sg.theme('DarkAmber')

#Function to send message to LED
def sendMorseCode(message):
    while True:
        for char in message:
            if char in morseCode:
                newCode = morseCode[char]
                for symbol in newCode:
                    if symbol == '.':
                        led.on()
                        print('LED ON')
                        sleep(0.2)  # This is the duration of the dot
                    elif symbol == '-':
                        led.on()
                        print('LED ON')
                        sleep(1)  # This is the duration of the dash
                    led.off()
                    print('LED OFF')
                    sleep(0.2)  # This will represent the gap between the code symbols
                sleep(1)  # This will represent the gap between the characters
            else:
                # Ignore non morse code characters
                continue
            sleep(2) # Pause at the end of the message

# Generate random numbers for 'numbers' list
numbers = []
for _ in range(5):
    randomNumber = random.randint(0, 9)
    numbers.append(randomNumber)
print("Starting numbers presented on the UI are", numbers)

# Generate random code for 'code' list
code = []
for _ in range(5):
    randomNumber2 = random.randint(0, 9)
    code.append(randomNumber2)
print("Code is", code)

# Convert 'code' list to a string
codeString = ''.join(str(num) for num in code)


#Layout of the UI is established using a series of container objects called frames that have been called using the PySimpleGUI import
#Additional fonts have been made available using the tkinter import
layout = [[sg.Frame('', layout=[], size=(1, 20))], [sg.T('   Enter Code below ... ', font=('Krungthep', 10))],

    [
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[0], font=("Krungthep", 60), key='Number0', pad=(
            10, 10))], [sg.Button('PRESS', key="Button0", font=('Kohinoor Telugu', 10) )]]),
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[1], font=("Krungthep", 60), key='Number1', pad=(
            10, 10))], [sg.Button('PRESS', key="Button1", font=('Kohinoor Telugu', 10))]]),
        sg.Frame('', element_justification ='center', layout=[[sg.T(numbers[2], font=("Krungthep", 60), key='Number2', pad=(
            10, 10))], [sg.Button('PRESS', key="Button2", font=('Kohinoor Telugu', 10))]]),
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[3], font=("Krungthep", 60), key='Number3', pad=(
            10, 10))], [sg.Button('PRESS', key="Button3", font=('Kohinoor Telugu', 10))]]),
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[4], font=("Krungthep", 60), key='Number4', pad=(
            10, 10))], [sg.Button('PRESS', key="Button4", font=('Kohinoor Telugu', 10))]])
    ],
    [
        #Displays correct code solution for testing purposes, should be commented out or removed during live game
        sg.T(code, font=("Kohinoor Telugu", 10)), 
        sg.Exit()
        
    ]
    
]

window = sg.Window("Key Pad", layout, size=(480, 320), element_justification='center', finalize=True)
window.Maximize()

def morse_code_thread():
    # Call sendMorseCode function with the code string
    sendMorseCode(codeString)

# Start the morse code thread
morse_thread = threading.Thread(target=morse_code_thread, daemon=True)
morse_thread.start()


while True:
    
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    elif event == 'Button0':  # This Button will control 1st, 2nd, 4th and 5th buttons
        numbers[0] += 1
        if numbers[0] > 9:
            numbers[0] = 0
      
        window['Number0'].update(numbers[0])
    
        # if statement used to give a clear indication that the code is correct
        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
            print("Numbers and code are the same")
            window['Number0'].update('C')
            window['Number1'].update('L')
            window['Number2'].update('E')
            window['Number3'].update('A')
            window['Number4'].update('R')
            
            #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
            GPIO.output(18, 0)

            #The for loop will iterate through each button and remove the visible button from the working UI upon completion to prevent further activity
            for buttonKeys in range(5): 
                window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")
            

    elif event == 'Button1':  # This Button will control 1st, 2nd and 3rd buttons
       
        numbers[1] += 1
        if numbers[1] > 9:
            numbers[1] = 0
       
        
        window['Number1'].update(numbers[1])
        

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
                    print("Numbers and code are the same")
                    window['Number0'].update('C')
                    window['Number1'].update('L')
                    window['Number2'].update('E')
                    window['Number3'].update('A')
                    window['Number4'].update('R')
                    
                    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
                    GPIO.output(18, 0)
                    
                    for buttonKeys in range(5):
                     window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")

    elif event == 'Button2':  # This Button will control 2st, 3rd and 4th buttons
       
        numbers[2] += 1
        if numbers[2] > 9:
            numbers[2] = 0
      
        window['Number2'].update(numbers[2])
       

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
                    print("Numbers and code are the same")
                    window['Number0'].update('C')
                    window['Number1'].update('L')
                    window['Number2'].update('E')
                    window['Number3'].update('A')
                    window['Number4'].update('R')
                    
                    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
                    GPIO.output(18, 0)
                    
                    for buttonKeys in range(5):
                     window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")    

    elif event == 'Button3':  # This Button will control the 4th button
        numbers[3] += 1
        if numbers[3] > 9:
            numbers[3] = 0

        window['Number3'].update(numbers[3])
        

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
                    print("Numbers and code are the same")
                    window['Number0'].update('C')
                    window['Number1'].update('L')
                    window['Number2'].update('E')
                    window['Number3'].update('A')
                    window['Number4'].update('R')
                    
                    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
                    GPIO.output(18, 0)
                    
                    for buttonKeys in range(5):
                     window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")    
    
    elif event == 'Button4':  # This Button will control 2nd, 3rd and 5th buttons
      
        numbers[4] += 1
        if numbers[4] > 9:
            numbers[4] = 0

        window['Number4'].update(numbers[4])

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
                    print("Numbers and code are the same")
                    window['Number0'].update('C')
                    window['Number1'].update('L')
                    window['Number2'].update('E')
                    window['Number3'].update('A')
                    window['Number4'].update('R')
                    
                     #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V (Opens lock)
                    GPIO.output(18, 0)
                    
                    for buttonKeys in range(5):
                     window['Button{}'.format(buttonKeys)].update(visible=False)

        else:
            print("Numbers and code are not the same")    
   

window.close()
