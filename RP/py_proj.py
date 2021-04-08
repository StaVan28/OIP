
import RPi.GPIO as GPIO
import time

#---------------------------------------------------

ledsGPIO = [24, 25, 8, 7, 12, 16, 20, 21]

#---------------------------------------------------

def onLed(curLed):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(curLed, GPIO.OUT)
    GPIO.output(curLed, True)

#---------------------------------------------------

def offLed(curLed):
    GPIO.output(curLed, False)
    GPIO.cleanup(curLed)

#---------------------------------------------------

def lightUp(ledNumber, period):

    curLed = ledsGPIO[ledNumber]

    onLed(curLed)
    time.sleep(period)
    offLed(curLed)

#---------------------------------------------------

def blink(ledNumber, blinkCount, blinkPeriod):
    for indx in range(blinkCount):
        lightUp(ledNumber, blinkPeriod)
        time.sleep(blinkPeriod)

#---------------------------------------------------

def runningLight(count, period):
    for indx_count in range(count):
        for indx_num in range(len(ledsGPIO)):
           lightUp(indx_num, period)

#---------------------------------------------------

def runningDark(count, period):
    for indx in range(len(ledsGPIO)):
        onLed(ledsGPIO[indx])

    for indx_count in range(count):
        for indx_num in range(len(ledsGPIO)):
            offLed(ledsGPIO[indx_num])
            time.sleep(period)
            onLed(ledsGPIO[indx_num])

    for indx in range(len(ledsGPIO)):
        offLed(ledsGPIO[indx])

#---------------------------------------------------

def decToBinList(decNumber):
    binNumber = list(bin(decNumber))
    binNumber = binNumber[2:]
    binNumber = [int(indx) for indx in binNumber]

    arrayZero = []
    for indxZero in range(len(ledsGPIO)):
        arrayZero.append(0)

    binNumber = arrayZero +  binNumber
    binNumber = binNumber[-8:]
    return binNumber

#---------------------------------------------------

def lightNumber(number, period=0.5):
    binNumber = []
    binNumber = decToBinList(number)
    binNumber = list(reversed(binNumber))

    for indx in range(len(ledsGPIO)):
        if binNumber[indx] == True:
            onLed(ledsGPIO[indx])

    time.sleep(period)

    for indx in range(len(ledsGPIO)):
        if binNumber[indx] == True:
            offLed(ledsGPIO[indx])   


#---------------------------------------------------

def runningPattern(pattern, direction):
    lightNumber(pattern)
    if direction > 0:
        while True:
            pattern = (pattern << 1) % 256 + int((pattern << 1) / 256)
            lightNumber(pattern)
    else:
        while True:
            pattern = (pattern >> 1) * 128 + int(pattern >> 1)
            lightNumber(pattern)
    GPIO.output(ledsGPIO, 0)
    GPIO.cleanup()

#---------------------------------------------------   

#blink(3, 5, 0.1)

#lightUp(7, 1)

#runningDark(3, 0.1)

#lightNumber(17, 1)

#runningPattern(123, 1)
