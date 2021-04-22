import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#----------------------------------------------------

DAC_PIN_LIST      = [26, 19, 13,  6,  5, 11,  9, 10]
POTENTIOMETR_PIN  = 17
CMP_OUT_PIN       = 4

GPIO.setup(POTENTIOMETR_PIN, GPIO.OUT)
GPIO.setup(DAC_PIN_LIST,     GPIO.OUT)
GPIO.setup(CMP_OUT_PIN,      GPIO.IN)

#----------------------------------------------------

def decToBinList(decNumber) :
    vector = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range (0, 8) :
        if (decNumber % 2) == 1 :
            vector[i] = True
        decNumber = decNumber // 2

        if decNumber == 0 :
            return vector
    
    return vector

def num2dac(number) :
    vector = decToBinList(number)
    GPIO.output (DAC_PIN_LIST, 0)

    for i in range (0, 8) :
        if vector[i] == True :
            GPIO.output (DAC_PIN_LIST [7 - i], True)


def search() :
    volt = 0

    for indx in range (0, 255) :
        num2dac(indx)
        time.sleep(0.0005)
        if GPIO.input(CMP_OUT_PIN) != True :
            volt = 3.3 * float (indx) / 255
            break
    
    return volt


def valueToVolt(value) :
    return 3.3 * float (value) / 255


def binSearch() :
    value = 0
    indx  = 128

    while True :
        num2dac(value)
        time.sleep(0.0005)

        if GPIO.input(CMP_OUT_PIN) == True :
            value += indx
        else :
            value -= indx

        indx = int(indx / 2)
        if indx == 0 :
            break

    if value < 0 :
        return 0

    return valueToVolt(value)

#----------------------------------------------------

GPIO.output(POTENTIOMETR_PIN, True)

lastVolt = 0
NewVolt  = 0

try:
    while True:    
        NewVolt = binSearch()

        if abs(NewVolt - lastVolt) > 1.0 / 255.0 :
            print(NewVolt, int (NewVolt * 255 / 3.3))
            lastVolt = NewVolt

finally:
    GPIO.output(DAC_PIN_LIST,     False)
    GPIO.output(POTENTIOMETR_PIN, False)
    GPIO.cleanup()

#----------------------------------------------------
