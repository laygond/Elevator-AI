# -----------------------------
#   USAGE
# -----------------------------
# python addressable_rgb_control.py --rgb 0,100,122

# DESCRIPTION:
# This script is used for debugging/learning-demo.
# Set color to each INDIVIDUAL pixels in an LED strip
# through Data Wired GPIO pins from command line.

# HARDWARE:
# - WS281X 5V addressable LED strip

# Python Packages needed:
#   sudo pip3 install rpi_ws281x
#   sudo pip3 install adafruit-circuitpython-neopixel
#   sudo python3 -m pip install --force-reinstall adafruit-blinka

# NOTE:
# Possible DataWired GPIOs in a RPi4 are 21,18,12,10 which means 
# you can control up to 4 addressable led strips. (10 & 12 need SPI enabled)

# Author: Bryan Laygond
# Website: http://www.laygond.com
# ------------------------------

#Import necessary packages
import argparse
# import RPi.GPIO as GPIO
from time import sleep
import board
import neopixel


#LED Strip Setup
TOTAL_LED_PIXELS = 10            # Number of leds in your strip
LED_GPIO = board.D18             # Data GPIO pin
# GPIO.setmode(GPIO.BCM)           # GPIO Numbers instead of board pin numbers
# GPIO.setup(LED_GPIO, GPIO.OUT)   # Set pin as output

#Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--rgb", type=str, default="",
	help=" RGB color format")
args = vars(ap.parse_args())

#Get Color
try: 
    if len(args["rgb"].split(',')) == 3:
        rgb = [int(c) for c in args["rgb"].split(',')]
        print("[INFO] RGB: ", rgb)
        sleep(0.01)
except:
    print("[ERROR] RGB format should be like --rgb 0,50,255")

#Set Color
pixels1 = neopixel.NeoPixel(LED_GPIO, TOTAL_LED_PIXELS, brightness=1) #brightness (0-1)
pixels1.fill(rgb)