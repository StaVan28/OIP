import RPi.GPIO as GPIO
import time

#----------------------------------------------------

GPIO.setmode(GPIO.BCM)

DAC_PIN_LIST      = [26, 19, 13,  6,  5, 11,  9, 10]
POTENTIOMETR_PIN  =  17
CMP_OUT_PIN       =  4

#----------------------------------------------------

GPIO.setup(POTENTIOMETR_PIN, GPIO.OUT)
GPIO.setup(DAC_PIN_LIST, GPIO.OUT)
GPIO.setup(CMP_OUT_PIN,  GPIO.IN)

#----------------------------------------------------

def decToBinList(decNumber):
    vector = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range (0, 8) :
        if (decNumber % 2) == 1 :
            vector[i] = True
        decNumber = decNumber // 2

        if decNumber == 0 :
            return vector
    
    return vector

def num2dac(number):
    vector = decToBinList(number)
    GPIO.output (DAC_PIN_LIST, 0)

    for i in range (0, 8):
        if vector[i] == True:
            GPIO.output (DAC_PIN_LIST [7 - i], True)

#----------------------------------------------------

GPIO.output(POTENTIOMETR_PIN, True)

voltage    = 0
newVoltage = 0

try:
    while True:
        for indx in range (0, 255) :
            num2dac(indx)
            time.sleep (0.0001)
            if GPIO.input(CMP_OUT_PIN) != True :
                newVoltage = 3.3 * float (indx) / 255
                break
        
        if abs (newVoltage - voltage) > 1.0 / 255.0 :
            print (newVoltage, int (newVoltage * 255 / 3.3))
            voltage = newVoltage

finally:
    GPIO.output(DAC_PIN_LIST,     False)
    GPIO.output(POTENTIOMETR_PIN, False)
    GPIO.cleanup()

#----------------------------------------------------
