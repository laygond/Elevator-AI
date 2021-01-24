# -----------------------------
#   USAGE
# -----------------------------
# python check_tag.py 
#
# DESCRIPTION:
# Reads continously UUID from NFC tags: cards, phones, etc
# Checks if a tag is registered in the group database and active.
# If tag is active then activate elevator cabin.
# Also, if tag is a phone then push NDEF data to a website. 
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# COPYRIGHT:
# Code may only be distributed through http://www.laygond.com any other methods
# of obtaining or distributing are prohibited
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

# Website that will be pushed to phone when tapped
phone_website = "https://www.instagram.com/laygond/"

# Verify Reader is available
clf = nfc.ContactlessFrontend()
sony_RCS380 = 'usb:054c:06c1'       # Product and Vendor ID
print("[INFO] Usb NFC Reader Connected: ", clf.open(sony_RCS380))

# Callback functions to push website if NFC tag is a phone
def send_ndef_message(llc):
    # this stage is only reached after a successful llc connection
    snep = nfc.snep.SnepClient(llc)
    snep.put_records([ndef.UriRecord(phone_website)])
    
def immediately():
    global started
    return time.time() - started > .5

def llcp_connected(llc):
    threading.Thread(target=send_ndef_message, args=(llc,)).start()
    return True    # False returns llc object to be handled
                # True otherwise

# Read csv uuid database and active group
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path,'groupData.csv')
f = open(csv_path)
data = csv.DictReader(f)

# Read NFC tag when tapped (preferred method)
tag  = clf.connect(rdwr={'on-connect': lambda tag: False})
uuid = str(binascii.hexlify(tag.identifier).decode()) 
            
# Check Tag
while True:
    try:
        # Read NFC tag when tapped (preferred method)
        tag  = clf.connect(rdwr={'on-connect': lambda tag: False})
        uuid = str(binascii.hexlify(tag.identifier).decode())

        # Check tag against data 
        for row in data:
            if uuid in row['UUID']:
                print(row)
                if row["Active"] == 'True':
                    print("[INFO] TRUE BABY")
                    #Welcome row["User"], led green, activate button panel
                    f.seek(0)
                    break
                else:
                    print("[INFO] FALSE BABY")  
                    f.seek(0)
                    #led red
                    break
        
        # Push website to phone otherwise end attempt
        global started
        started = time.time()
        print("about to push")
        clf.connect(llcp={'on-connect':llcp_connected, 'lto':250, 'role':'initiator'}, terminate=immediately) 
        print("done pushing")
    except:
        pass

