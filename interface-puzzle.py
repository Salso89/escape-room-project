import PySimpleGUI as sg
import random
import functools
from tkinter import *

#Sets colour scheme for the UI pop up
sg.theme('DarkTeal12')

numbers = []
for int in range(5):
    randomNumber = random.randint(0, 9)
    numbers.append(randomNumber)
print("Starting numbers presented on the UI are", numbers)

code = []
for int in range(5):
    randomNumber2 = random.randint(0, 9)
    code.append(randomNumber2)
print("Code is", code)

layout = [[sg.Frame('', layout=[], size=(1, 40))], [sg.T('Enter Code below ... ', font=('Impact', 50))],

    
    [
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[0], font=("Krungthep", 175), key='Number0', pad=(
            10, 10))], [sg.Button('PRESS', key="Button0", font=('Kohinoor Telugu', 20) )]]),
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[1], font=("Krungthep", 175), key='Number1', pad=(
            10, 10))], [sg.Button('PRESS', key="Button1", font=('Kohinoor Telugu', 20))]]),
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[2], font=("Krungthep", 175), key='Number2', pad=(
            10, 10))], [sg.Button('PRESS', key="Button2", font=('Kohinoor Telugu', 20))]]),
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[3], font=("Krungthep", 175), key='Number3', pad=(
            10, 10))], [sg.Button('PRESS', key="Button3", font=('Kohinoor Telugu', 20))]]),
        sg.Frame('', element_justification='center', layout=[[sg.T(numbers[4], font=("Krungthep", 175), key='Number4', pad=(
            10, 10))], [sg.Button('PRESS', key="Button4", font=('Kohinoor Telugu', 20))]])
    ],
    [
        sg.T(code, font=("Kohinoor Telugu", 20)),
        
    ]
]

window = sg.Window("Number Puzzle", layout, size=(800, 480),
                   element_justification='center', finalize=True)
window.Maximize()

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'EXIT'):
        break
    elif event == 'Button0':  # This Button will control 1st, 2nd, 4th and 5th buttons
        numbers[0] += 1
        if numbers[0] > 9:
            numbers[0] = 0
        numbers[1] += 1
        if numbers[1] > 9:
            numbers[1] = 0
        numbers[3] += 1
        if numbers[3] > 9:
            numbers[3] = 0
        numbers[4] += 1
        if numbers[4] > 9:
            numbers[4] = 0

        window['Number0'].update(numbers[0])
        window['Number1'].update(numbers[1])
        window['Number3'].update(numbers[3])
        window['Number4'].update(numbers[4])

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
            print("Numbers and code are the same")
            window['Number0'].update('C')
            window['Number1'].update('L')
            window['Number2'].update('E')
            window['Number3'].update('A')
            window['Number4'].update('R')
            for buttonKeys in range(5):
                        window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")

    elif event == 'Button1':  # This Button will control 1st, 2nd and 3rd buttons
        numbers[0] += 1
        if numbers[0] > 9:
            numbers[0] = 0
        numbers[1] += 1
        if numbers[1] > 9:
            numbers[1] = 0
        numbers[2] += 1
        if numbers[2] > 9:
            numbers[2] = 0

        window['Number0'].update(numbers[0])
        window['Number1'].update(numbers[1])
        window['Number2'].update(numbers[2])

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
                    print("Numbers and code are the same")
                    window['Number0'].update('C')
                    window['Number1'].update('L')
                    window['Number2'].update('E')
                    window['Number3'].update('A')
                    window['Number4'].update('R')
                    for buttonKeys in range(5):
                        window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")

    elif event == 'Button2':  # This Button will control 2st, 3rd and 4th buttons
        numbers[1] += 1
        if numbers[1] > 9:
            numbers[1] = 0
        numbers[2] += 1
        if numbers[2] > 9:
            numbers[2] = 0
        numbers[3] += 1
        if numbers[3] > 9:
            numbers[3] = 0

        window['Number1'].update(numbers[1])
        window['Number2'].update(numbers[2])
        window['Number3'].update(numbers[3])

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
                    print("Numbers and code are the same")
                    window['Number0'].update('C')
                    window['Number1'].update('L')
                    window['Number2'].update('E')
                    window['Number3'].update('A')
                    window['Number4'].update('R')
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
                    for buttonKeys in range(5):
                        window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")    
    
    elif event == 'Button4':  # This Button will control 2nd, 3rd and 5th buttons
        numbers[1] += 1
        if numbers[1] > 9:
            numbers[1] = 0
        numbers[2] += 1
        if numbers[2] > 9:
            numbers[2] = 0
        numbers[4] += 1
        if numbers[4] > 9:
            numbers[4] = 0

        window['Number1'].update(numbers[1])
        window['Number2'].update(numbers[2])
        window['Number4'].update(numbers[4])

        if functools.reduce(lambda x, y: x and y, map(lambda p, q: p == q, numbers, code), True):
                    print("Numbers and code are the same")
                    window['Number0'].update('C')
                    window['Number1'].update('L')
                    window['Number2'].update('E')
                    window['Number3'].update('A')
                    window['Number4'].update('R')
                    for buttonKeys in range(5):
                        window['Button{}'.format(buttonKeys)].update(visible=False)
        else:
            print("Numbers and code are not the same")    
    
window.close()
