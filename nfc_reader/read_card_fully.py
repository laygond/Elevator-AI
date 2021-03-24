# -----------------------------
#   USAGE
# -----------------------------
# python read_card_fully.py 
# 
# DESCRIPTION:
# Reads continously and thoroughly everythig from NFC card tags (not phones)
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# COPYRIGHT:
# Code may only be distributed through http://www.laygond.com or GitHub @laygond
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

# Verify Reader is available
clf = nfc.ContactlessFrontend()
sony_RCS380 = 'usb:054c:06c1'       # Product and Vendor ID
print("[INFO] Usb NFC Reader Connected: ", clf.open(sony_RCS380))

# # Sense and activate NFC tag instantaneously (fails if tag is not on reader) 
# from nfc.clf import RemoteTarget
# target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
# print(target)
# tag = nfc.tag.activate(clf, target)
# print(tag)

while True:
    try:
        # Connect: Sense and activate NFC tag when tapped (preferred method)
        # More Parameters here: https://nfcpy.readthedocs.io/en/latest/modules/tag.html#nfc.tag.Tag
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print("[INFO] General:", tag)
        print("[INFO] UID:", binascii.hexlify(tag.identifier).decode())
        print("[INFO] Card Struct:")
        print("\n".join(["\t" + line for line in tag.dump()]))
        if tag.ndef is not None: 
            print("[INFO] NDEF Records:")
            for record in tag.ndef.records:
                print(record)
            # # Alternative method
            # # More parameters here: https://ndeflib.readthedocs.io/en/latest/records/smartposter.html
            # record = tag.ndef.records[0]
            # print(record.resource)
            # print(record.type)

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        pass
    

