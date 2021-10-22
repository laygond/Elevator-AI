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
r.start(0)
g.start(0)
b.start(0)

# Website that will be pushed to phone when tapped
phone_website = "https://condominioimbabura.github.io/"

# MQTT Setup
mqttBroker ="192.168.0.205" 
client = mqtt.Client("PyMQ")
client.connect(mqttBroker)

# Verify Reader is available
clf = nfc.ContactlessFrontend()
sony_RCS380 = 'usb:054c:06c1'       # Product and Vendor ID
print("[INFO] Usb NFC Reader Connected: ", clf.open(sony_RCS380))  # never comment out

# Callback functions to push website if NFC tag is a phone
def send_ndef_message(llc):
    # this stage is only reached after a successful llc connection
    snep = nfc.snep.SnepClient(llc)
    snep.put_records([ndef.UriRecord(phone_website)])
    
def immediately():
    global phone_started
    return time.time() - phone_started > .5

def llcp_connected(llc):
    threading.Thread(target=send_ndef_message, args=(llc,)).start()
    return True     # False returns llc object to be handled
                    # True otherwise


# Callback to turn on and off LED Strip
def led_signal(channel):
    channel.ChangeDutyCycle(100)
    time.sleep(.8)
    channel.ChangeDutyCycle(0)


# Set csv path point to active group and pickle path to enable 
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path,'groupData.csv')
pickle_path = os.path.join(dir_path,'../botonera/enable')

# Callback to Disable Button Pannel after 5 seconds 
# (Set enable pickle file to false)
def disable_button_panel(time_since_enable_started):
    while(time.time() - time_since_enable_started < 5): pass      # hold time for t seconds
    print(time.strftime("%H %M %S",time.localtime()))
    # p = open(pickle_path,'rwb')
    # botonera_enabled_through_tag = pickle.load(p)
    # if botonera_enabled_through_tag:
    #     botonera_enabled_through_tag = False
    #     pickle.dump(botonera_enabled_through_tag,p)
    # p.close()


# Read NFC tag when tapped (preferred method) (first instances of variables)
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
        for row in data:
            if uuid in row['UUID']:
                #print(row)
                if row["Active"] == 'True':
                    print("[INFO]=== TAG IS ACTIVE ===")                    
                    # Enable Button Panel
                    p = open(pickle_path,'wb')
                    botonera_enabled_through_tag= True
                    pickle.dump(botonera_enabled_through_tag, p)
                    p.close()

                    # Track time and disable Button Pannel after 5 seconds
                    threading.Thread(target=disable_button_panel, args=(time.time(),)).start()

                    # GREEN light
                    threading.Thread(target=led_signal, args=[g]).start() 
                    
                    # Reset file pointer
                    f.seek(0)
                    break
                else:
                    print("[INFO]=== PAY YOUR BILLS BABY ===")    
                    # RED light
                    threading.Thread(target=led_signal, args=(r,)).start()

                    # Reset file pointer
                    f.seek(0)
                    break
        
        # Push website to phone otherwise end attempt
        global phone_started
        phone_started = time.time()
        #print("about to push")
        clf.connect(llcp={'on-connect':llcp_connected, 'lto':250, 'role':'initiator'}, terminate=immediately) 
        #print("done pushing")
  
    except:
        pass

