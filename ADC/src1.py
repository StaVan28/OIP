import RPi.GPIO as GPIO
import time

#----------------------------------------------------

GPIO.setmode(GPIO.BCM)

DAC_PIN_LIST     = [26, 19, 13,  6,  5, 11,  9, 10]
POTENTIOMETR_PIN = 17

#----------------------------------------------------

GPIO.setup(POTENTIOMETR_PIN, GPIO.OUT)
GPIO.setup(DAC_PIN_LIST, GPIO.OUT)

#----------------------------------------------------

def decToBinList(decNumber) :
    vector = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range (0, 8) :
        if (decNumber % 2) == True :
            vector [i] = True
        decNumber = decNumber // 2

        if decNumber == 0 :
            return vector
    
    return vector

def num2dac(number) :
    vector = decToBinList(number)
    GPIO.output(DAC_PIN_LIST, False)

    for i in range (0, 8) :
        if vector [i] == True :
            GPIO.output(DAC_PIN_LIST [7 - i], True)

#----------------------------------------------------

GPIO.output(POTENTIOMETR_PIN, True)

while True:
    try:
        print("Enter value (-1 to exit) > ")
        num = int (input())

        if num == -1:
            break

    finally:
        if num != -1:
            print(num, "=", 3.3 * float (num) / 255, "V")
            num2dac(num)

#----------------------------------------------------

GPIO.output(DAC_PIN_LIST,     False)
GPIO.output(POTENTIOMETR_PIN, False)
GPIO.cleanup()