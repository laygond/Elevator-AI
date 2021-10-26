# -----------------------------
#   USAGE
# -----------------------------
# python check_tag.py 
#
# DESCRIPTION:
# Reads continously UUID from NFC tags: cards, phones, etc
# Checks if a tag is registered in the group database and active.
# If tag is active then set as true the 'enable' pickle file at 'Elevator-AI/botonera'.
# which indicates temporal access to the elevator's button panel. 
# An LED strip for visual notification is turned on (green=active or red=non-active)
# Also, any tag UUID is sent as an MQTT message to openhab's server for record.
# Also, if tag is a phone then push NDEF data to a website. 
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# COPYRIGHT:
# Code may only be distributed through
# http://www.laygond.com or https://github.com/laygond
# any other methods of obtaining or distributing are prohibited
# Copyright (c) 2020-2021
#
# NOTE:
# NFC Reader must be given access rights before running code as mentioned:
# https://nfcpy.readthedocs.io/en/latest/topics/get-started.html#installation
#
# HARDWARE (Modify to your needs):
# - Sony RC-S380            https://www.sony.net/Products/felica/business/tech-support/
# - Card NTAG215 type 2     https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf
# - L298N as LED driver     https://sudonull.com/post/111051-RGB-tape-control-with-Arduino-and-L298N-driver
# ------------------------------

# Import the necessary packages
import csv
import nfc
import ndef
import threading
import binascii
import time
import os
import paho.mqtt.client as mqtt 
import RPi.GPIO as GPIO
import pickle

# LED Strip Setup for visual notification
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
r.start(100)                       # Active Low setup since L298N
g.start(100)
b.start(100)

# MQTT Setup
mqttBroker ="192.168.0.205" 
client = mqtt.Client("PyMQ")
client.connect(mqttBroker)

# Set path to files 
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path,'groupData.csv')
pickle_path  = os.path.join(dir_path,'../botonera/enable')

# Callback to turn on and off LED Strip
def led_signal(channel):
    channel.ChangeDutyCycle(0)
    time.sleep(.6)
    channel.ChangeDutyCycle(100)

# Global Timer variable that reintializes with every tap
button_panel_timer = 0

# Callback to Disable Button Pannel after 5 seconds from latest tap
def disable_button_panel():
    local_timer_start = time.time()
    while(time.time() - local_timer_start < 5): pass      # hold time for t seconds
    if time.time() - button_panel_timer > 5: 
        p = open(pickle_path,'wb')
        botonera_enabled_through_tag = False
        pickle.dump(botonera_enabled_through_tag,p)
        p.close()

# Setup NFC Reader and Read NFC tag when tapped
clf = nfc.ContactlessFrontend()
sony_RCS380 = 'usb:054c:06c1'       # Product and Vendor ID
print("[INFO] Usb NFC Reader Connected: ", clf.open(sony_RCS380))  # never comment out
tag  = clf.connect(rdwr={'on-connect': lambda tag: False})
uuid = str(binascii.hexlify(tag.identifier).decode()) 
            
# Check Tag
while True:
    try:
        # Read NFC tag when tapped (preferred method)
        tag  = clf.connect(rdwr={'on-connect': lambda tag: False})
        uuid = str(binascii.hexlify(tag.identifier).decode())

        # Send uuid to openhab server for record purposes
        client.reconnect() # in case broker disconnects
        client.publish("elevator/sensor/nfc", uuid)

        # Check tag against data
        f = open(csv_path)
        data = csv.DictReader(f)
        tag_found = False 
        for row in data:
            if uuid in row['UUID']:
                #print(row)
                tag_found = True
                if row["Active"] == 'True':
                    #print("[INFO]=== TAG IS ACTIVE ===")                    
                    # GREEN light
                    threading.Thread(target=led_signal, args=[g]).start()

                    # Enable Button Panel
                    p = open(pickle_path,'wb')
                    botonera_enabled_through_tag= True
                    pickle.dump(botonera_enabled_through_tag, p)
                    p.close()
                    
                    # Reset file pointer
                    f.seek(0)           
                    
                    # Keep Track of time if no button is pressed: disable Button Pannel in 5 seconds
                    button_panel_timer= time.time()     # Reset time with every active tag
                    threading.Thread(target=disable_button_panel).start()                    
                    break

                else:
                    #print("[INFO]=== PAY YOUR BILLS BABY ===")    
                    # RED light
                    threading.Thread(target=led_signal, args=[r]).start()

                    # Reset file pointer
                    f.seek(0)
                    break

        # BLUE light: New Tag has been scanned
        if not tag_found:        
            threading.Thread(target=led_signal, args=[b]).start()
    except:
        pass

