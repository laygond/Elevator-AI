# -----------------------------
#   USAGE
# -----------------------------
# python presionar_boton.py --input 'B1' --switch 'ON'
#
# DESCRIPTION:
# Simulates the press of a button from the elevator button panel through relays.
# This script is run in response to clicking on any button from Openhab's Habpanel "Botonera."
# Before relay activation it checks whether the panel is enabled or if a floor has
# special permission schedule.
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# COPYRIGHT:
# Code may only be distributed through
# http://www.laygond.com or https://github.com/laygond
# any other methods of obtaining or distributing are prohibited
# Copyright (c) 2020-2021
# ------------------------------

# Import necessary packages
import datetime
import time
import argparse
import os, sys 
import RPi.GPIO as GPIO
import pickle

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Button to Press in Elevator")
ap.add_argument("-s", "--switch", type=str, default="",
	help=" Switch State")
args = vars(ap.parse_args())

# Relay Setup to enable elevator button panel
GPIO.setmode(GPIO.BCM)         # GPIO Numbers instead of board pin numbers
GPIO.setwarnings(False)        # In case  pin is set to output twice
GPIO_ON  = 0                   # Since my relay is active low
GPIO_OFF = 1
RELAY_PIN = {
'BPB' : 18,               # Relay pins from button PB (lobby) to button 9 (ninth floor)
'B1'  : 17,               # These are single press ON buttons
'B2'  : 27,
'B3'  : 5,
'B4'  : 5,
'B5'  : 5,
'B6'  : 5,
'B7'  : 5,
'B8'  : 5,
'B9'  : 5,
'BDetener' : 22,          # Relay pins for stopping elevator cabin and alarm
'BAlarma'  : 23}          # These are ON/OFF switches (double state buttons) 
GPIO.setup(RELAY_PIN[args['input']], GPIO.OUT)    # Set pin as output     
GPIO.output(RELAY_PIN[args['input']], GPIO_OFF)   # Start with relay off

# Path to pickle file
dir_path    = os.path.dirname(os.path.realpath(__file__))
pickle_path = os.path.join(dir_path,'enable')

# Get permission results from tap-tag verification
p = open(pickle_path,'rb')
botonera_enabled_through_tag = pickle.load(p)
p.close()

# Special Floor Permissions
def floor4_permission():
    # Weekdays Between 12-2PM
    today = datetime.datetime.today()
    d = today.weekday() # Monday-Sunday (0-6)
    t = today.time()
    if d<5 and datetime.time(12)< t <datetime.time(14):
        return True
    return False


# Helper Functions
def press(GPIO_pin):
    GPIO.output(GPIO_pin, GPIO_ON) #Press Button Panel
    time.sleep(0.4) # less than half second
    GPIO.output(GPIO_pin, GPIO_OFF)#Release Button Panel

def long_press(GPIO_pin):
    GPIO.output(GPIO_pin, GPIO_ON) 
    time.sleep(5)     # 5 second
    GPIO.output(GPIO_pin, GPIO_OFF)

def disable_button_panel():
    botonera_enabled_through_tag = False
    p = open(pickle_path,'wb')
    pickle.dump(botonera_enabled_through_tag,p)
    p.close()


# Press Button based on triggering item's name
if args["input"] == 'BPB':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['BPB'])         #Press Button Panel
        disable_button_panel()  #no longer needs to be enabled

if args["input"] == 'B1':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['B1'])         
        disable_button_panel()  

# if args["input"] == 'B2': # THIS FLOOR IS UNAVAILABLE FOR PRIVATE REASONS
#     if botonera_enabled_through_tag:
#         press(RELAY_PIN['B2'])         
#         disable_button_panel() 

if args["input"] == 'B3':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['B3'])         
        disable_button_panel() 
        
if args["input"] == 'B4':
    if botonera_enabled_through_tag or floor4_permission():
        press(RELAY_PIN['B4'])         
        disable_button_panel() 
        
if args["input"] == 'B5':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['B5'])         
        disable_button_panel()  
        
if args["input"] == 'B6':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['B6'])         
        disable_button_panel()  
        
if args["input"] == 'B7':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['B7'])         
        disable_button_panel()  
        
if args["input"] == 'B8':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['B8'])         
        disable_button_panel()  
        
if args["input"] == 'B9':
    if botonera_enabled_through_tag:
        press(RELAY_PIN['B9'])         
        disable_button_panel()  
    
if args["input"] == 'BDetener':
    if args["switch"] == 'ON':
        press(RELAY_PIN['BDetener']) 
    if args["switch"] == 'OFF':
        GPIO.setup(RELAY_PIN['BPB'], GPIO.OUT)
        GPIO.output(RELAY_PIN['BPB'], GPIO_OFF)
        press(RELAY_PIN['BPB'])    # Send back to Lobby (Can be any button to make it move)
        GPIO.setup(RELAY_PIN['BPB'], GPIO.IN)
        disable_button_panel()  
	
if args["input"] == 'BAlarma':
    long_press(RELAY_PIN['BAlarma'])          

# Set GPIO pin back to default
GPIO.setup(RELAY_PIN[args['input']], GPIO.IN)    # Set pin as input

