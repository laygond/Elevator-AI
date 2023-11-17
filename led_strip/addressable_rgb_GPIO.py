# -----------------------------
#   USAGE
# -----------------------------
# python addressable_rgb_GPIO.py --rgb 0,100,122

# DESCRIPTION:
# This script is used for debugging/learning-demo.
# Set color to each INDIVIDUAL pixels in an LED strip
# through Data Wired GPIO pins from command line.

# HARDWARE:
# - WS281X 5V addressable LED strip

# Python Packages needed:
#   sudo pip3 install RPi.WS281X

# NOTE:
# - Possible DataWired GPIOs in a RPi4 are 21,18,12,10 which means 
# you can control up to 4 addressable led strips. (10 & 12 need SPI enabled)

# Author: Bryan Laygond
# Website: http://www.laygond.com
# ------------------------------


#Import necessary packages
import RPi.GPIO as GPIO
import time
import argparse

#Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--rgb", type=str, default="",
	help=" RGB color format")
args = vars(ap.parse_args())

# LED Strip Setup
NUM_LEDS = 10 #  number of LEDs on the strip
DATA_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.OUT)

#====== HELPER FUNCTIONS ======
# Define a function to send a single bit to the LED strip
def send_bit(bit):
  if bit == 1:
    GPIO.output(DATA_PIN, GPIO.HIGH)
    time.sleep(0.35 * 10**-6)
    GPIO.output(DATA_PIN, GPIO.LOW)
    time.sleep(1.65 * 10**-6)
  else:
    GPIO.output(DATA_PIN, GPIO.HIGH)
    time.sleep(0.85 * 10**-6)
    GPIO.output(DATA_PIN, GPIO.LOW)
    time.sleep(1.15 * 10**-6)

# Define a function to send a byte to the LED strip
def send_byte(byte):
  for bit in range(7, -1, -1):
    send_bit((byte >> bit) & 1)

# Define a function to send a color to a pixel in LED strip
def set_pixel(color):
  send_byte(color[0] >> 8)
  send_byte(color[0] & 0xFF)
  send_byte(color[1] >> 8)
  send_byte(color[1] & 0xFF)
  send_byte(color[2] >> 8)
  send_byte(color[2] & 0xFF)

# Send the color to entire the LED strip
def set_all_leds(color):
    for i in range(NUM_LEDS):
        set_pixel(color)
    time.sleep(0.01)

# Define a function to clear the LED strip
def clear_strip():
  for i in range(NUM_LEDS):
    set_pixel((0, 0, 0))

#==================================

#Get Color
try: 
    if len(args["rgb"].split(',')) == 3:
        rgb = [int(c) for c in args["rgb"].split(',')]
        print("[INFO] RGB: ", rgb)
        time.sleep(0.01)
except:
    print("[ERROR] RGB format should be like --rgb 0,50,255")

#Set Color
set_all_leds(rgb)

