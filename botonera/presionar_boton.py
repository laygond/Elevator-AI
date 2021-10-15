import time
import argparse
import os, sys 
import RPi.GPIO as GPIO

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Button to Press in Elevator")
args = vars(ap.parse_args())

# Relay Setup to enable elevator button panel
GPIO.setmode(GPIO.BCM)              # GPIO Numbers instead of board pin numbers
RELAY_GPIO = 17
GPIO_ON  = 0                        # Since my relay is active low
GPIO_OFF = 1
GPIO.setup(RELAY_GPIO, GPIO.OUT)    # Set pin as output
GPIO.output(RELAY_GPIO, GPIO_OFF)   # Start with relay off

if args["input"] == 'B2':
    GPIO.output(RELAY_GPIO, GPIO_ON) #Press Button Panel
    time.sleep(0.4) # less than half second
    GPIO.output(RELAY_GPIO, GPIO_OFF) #Release Button Panel

if args["input"] == 'B4':
    GPIO.output(RELAY_GPIO, GPIO_ON) #Press Button Panel
    time.sleep(0.4) # less than half second
    GPIO.output(RELAY_GPIO, GPIO_OFF) #Release Button Panel