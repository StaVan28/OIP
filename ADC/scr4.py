import RPi.GPIO as GPIO
import time

#----------------------------------------------------

GPIO.setmode(GPIO.BCM)

DAC_PIN_LIST      = [26, 19, 13,  6,  5, 11,  9, 10]
DIODS_PIN_LIST    = [21, 20, 16, 12,  7,  8, 25, 24]
POTENTIOMETR_PIN  = 17
CMP_OUT_PIN       = 4

GPIO.setup(DAC_PIN_LIST,     GPIO.OUT)
GPIO.setup(DIODS_PIN_LIST,   GPIO.OUT)
GPIO.setup(POTENTIOMETR_PIN, GPIO.OUT)

GPIO.setup(CMP_OUT_PIN, GPIO.IN)


#----------------------------------------------------

def decToBinList(decNumber) :
    vector = [0, 0, 0, 0, 0, 0, 0, 0]

    for indx in range(len(vector)) :
        if (decNumber % 2) == True :
            vector[indx] = True

        decNumber = decNumber // 2

        if decNumber == 0 :
            return vector
    
    return vector

def num2dac(number) :
    vector = decToBinList(number)

    GPIO.output(DAC_PIN_LIST, False)

    for indx in range(len(DAC_PIN_LIST)) :
        if vector[indx] == True :
            GPIO.output(DAC_PIN_LIST [7 - indx], True)


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

def voltToValue(volt) :
    return int (255 * value / 3.3)


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

def num2VolLvl(volt) :
    vec = [0, 0, 0, 0, 0, 0, 0, 0]

    number = voltToValue(volt)

    print("number = ", number)
    
    if (number >= 252):
        vec =  [1, 1, 1, 1, 1, 1, 1, 1]
    elif (number > 256 / 8 * 4):
        vec  = [0, 0, 0, 0, 1, 1, 1, 1]
    else:
        vec  = [0, 0, 0, 0, 0, 0, 0, 0]

    GPIO.output(DIODS_PIN_LIST, False)

    for indx in range(len(DIODS_PIN_LIST)) :
        if vec[indx] == True :
            GPIO.output(DIODS_PIN_LIST[7 - indx], True)

#----------------------------------------------------

GPIO.output(POTENTIOMETR_PIN, True)

value = 0

try:
    while True:
        value = binSearch()
        num2VolLvl(value)
        print(value)

finally:
    GPIO.output(DIODS_PIN_LIST,   False)
    GPIO.output(DAC_PIN_LIST,     False)
    GPIO.output(POTENTIOMETR_PIN, False)
    GPIO.cleanup()

#----------------------------------------------------