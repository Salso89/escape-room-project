from gpiozero import LED
from time import sleep

#Assigning LED to board number (BCM)
led = LED(23)

#Assign morse code values
morseCode = {
    
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
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
                        sleep(1)  # This is duration of the dash
                    led.off()
                    print('LED OFF')
                    sleep(0.2)  # This will represent the gap bewtween the code symbols
                sleep(1)  # This will represent the gap between the characters
            else:
                # Ignore non morse code characters
                continue
            sleep(2) #pause at the end of the message


message = '1, 2, 3, 4' #Hard code message
sendMorseCode(message) #Call function
