# -----------------------------
#   USAGE
# -----------------------------
# python classic_rgb_control.py --rgb 0,100,122
#
# DESCRIPTION:
# This script is used for debugging/learning-demo.
# Set color of an ENTIRE non-addressable LED strip
# through PWM from command line.
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
# ------------------------------

# Import necessary packages
import argparse
import RPi.GPIO as GPIO
from time import sleep

# LED Strip Setup
GPIO.setmode(GPIO.BCM)             # GPIO Numbers instead of board pin numbers
LED_R_GPIO = 2                     # Red pin
LED_G_GPIO = 3                     # Green pin
LED_B_GPIO = 4                     # Blue pin
GPIO.setup(LED_R_GPIO, GPIO.OUT)   # Set pin as output
GPIO.setup(LED_G_GPIO, GPIO.OUT)    
GPIO.setup(LED_B_GPIO, GPIO.OUT)    
r = GPIO.PWM(LED_R_GPIO, 100)      # PWM from 0-100
g = GPIO.PWM(LED_G_GPIO, 100)
b = GPIO.PWM(LED_B_GPIO, 100)
r.start(0)
g.start(0)
b.start(0)

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--rgb", type=str, default="",
	help=" RGB color format")
args = vars(ap.parse_args())

# Set Color
try: 
    if len(args["rgb"].split(',')) == 3:
        rgb = [int(float(c)/255*100) for c in args["rgb"].split(',')]
        print("[INFO] In percentage (0-100)% RGB: ", rgb)
        r.ChangeDutyCycle(rgb[0])
        g.ChangeDutyCycle(rgb[1])
        b.ChangeDutyCycle(rgb[2])
        sleep(0.01)
except:
    print("[ERROR] RGB format should be like --rgb 0,50,255")

