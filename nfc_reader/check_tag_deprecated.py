# -----------------------------
#   USAGE (DEPRECATED: Left for educational purposes)
# -----------------------------
# python check_tag_deprecated.py 
#
# DESCRIPTION:
# Reads continously UUID from NFC tags: cards, phones, etc
# Checks if a tag is registered in the group database and active.
# If tag is active then enable through a relay the elevator button pannel.
# Mqtt messages are sent to an LED strip for visual notification (green or red)
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

# Relay Setup to enable elevator button panel
relay_started = time.time()         # keep track of time when relay on
GPIO.setmode(GPIO.BCM)              # GPIO Numbers instead of board pin numbers
RELAY_GPIO = 17
GPIO_ON  = 0                        # Since my relay is active low
GPIO_OFF = 1
GPIO.setup(RELAY_GPIO, GPIO.OUT)    # Set pin as output
GPIO.output(RELAY_GPIO, GPIO_OFF)   # Start with relay off

# Website that will be pushed to phone when tapped
phone_website = "https://condominioimbabura.github.io/"

# MQTT Setup
mqttBroker ="192.168.0.205" 
client = mqtt.Client("PythonMQTT")
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

# Set csv path point to active group
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path,'groupData.csv')

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
                    #print("[INFO] TRUE BABY")
                    client.reconnect() # in case broker disconnects
                    client.publish("elevator/control/led", "0;100;0") #GREEN light 
                    GPIO.output(RELAY_GPIO, GPIO_ON) #Enable Button Panel and track time
                    relay_started = time.time()
                    f.seek(0)
                    break
                else:
                    #print("[INFO] FALSE BABY") 
                    client.reconnect() # in case broker disconnects   
                    client.publish("elevator/control/led", "100;0;0") #RED light
                    f.seek(0)
                    break
        
        # Push website to phone otherwise end attempt
        global phone_started
        phone_started = time.time()
        #print("about to push")
        clf.connect(llcp={'on-connect':llcp_connected, 'lto':250, 'role':'initiator'}, terminate=immediately) 
        #print("done pushing")

        # Disable Button Pannel after 3 seconds (Set Relay off)
        while(time.time() - relay_started < 3): pass      # hold time for t seconds
        GPIO.output(RELAY_GPIO, GPIO_OFF) 

    except:
        pass

