# -----------------------------
#   USAGE
# -----------------------------
# python read_write_add2DB.py --output database.cvs --write 1 
#
# DESCRIPTION:
# Reads continously UUID from NFC tags: cards, phones, etc
# If an output file is provided then each UUID entry is added to the DataBase
# The code automatically prevents UUID duplicates or classic phone errors such as 11223344 
# If the write flag is on then provided NDEF records are written to every card scanned
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
import argparse
import numpy as np

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output database file")
ap.add_argument("-w", "--write", type=int, default=0,
	help="whether or not write NDEF records to cards")
args = vars(ap.parse_args())

# NDEF Records to be written on cards (Modify to your needs)
website = "http://www.laygond.com"
title   = "LAYGOND-AI Condominio Imbabura"

# Verify Reader is available
clf = nfc.ContactlessFrontend()
sony_RCS380 = 'usb:054c:06c1'       # Product and Vendor ID
print("[INFO] Usb NFC Reader Connected: ", clf.open(sony_RCS380))

# Open/Create DB Output File as list
if args["output"] != "" :
    f = open(args["output"], 'a')
    uuid_db = open(args["output"]).read().strip().split("\n")


try:
    while True:
        # Read
        # More Parameters here: https://nfcpy.readthedocs.io/en/latest/modules/tag.html#nfc.tag.Tag
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print("[INFO] General:", tag)
        uuid = binascii.hexlify(tag.identifier).decode()
        print("[INFO] UID:", uuid)

        # Add to Database list
        if args["output"] != "" :
            if uuid == "11223344":
                print("[INFO] Phone ID Ignored")
            elif uuid in uuid_db:
                print("[INFO] Duplicate Found")
            else:
                uuid_db.append(uuid)
                f.write(uuid + '\n')

        # Write NDEF records to tag
        if args["write"] > 0:
            try:
                if tag.ndef is not None: 
                    tag.ndef.records = [ndef.SmartposterRecord(website, title)] 
                    print("[INFO] Write NDEF Complete!" )
            except:
                print("[WARNING] Cannot write NDEF record to phone")
      
except:
    pass

