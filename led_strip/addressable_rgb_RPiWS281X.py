# -----------------------------
#   USAGE
# -----------------------------
# python addressable_rgb_RPiWS281X.py --rgb 0,100,122

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

import time
import RPi.WS281X as ws

# Define the GPIO pin connected to the data pin of the LED strip
DATA_PIN = 18

# Set the number of LEDs in the strip
NUM_LEDS = 10

# Initialize the ws281x library
ws.init(DATA_PIN, NUM_LEDS)

# Define a function to set the color of all LEDs to a specific color
def set_all_leds(color):
    for i in range(NUM_LEDS):
        ws.set_pixel(i, color)

# Define a function to clear the LED strip
def clear_strip():
    for i in range(NUM_LEDS):
        ws.set_pixel(i, (0, 0, 0))

# Set the brightness of the LEDs
brightness = 0.5

# Main loop
while True:
    # Set all LEDs to red
    set_all_leds((255, 0, 0))

    # Wait for a short period of time
    time.sleep(0.5)

    # Set all LEDs to green
    set_all_leds((0, 255, 0))

    # Wait for a short period of time
    time.sleep(0.5)

    # Set all LEDs to blue
    set_all_leds((0, 0, 255))

    # Wait for a short period of time
    time.sleep(0.5)

    # Clear the LED strip
    clear_strip()
