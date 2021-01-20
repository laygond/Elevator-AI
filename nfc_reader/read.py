import csv
import nfc
import ndef
import threading
import binascii
import time

# Tag: A card or phone is considered an NFC tag 

# NFC Reader must be given access rights before running code as mentioned:
# https://nfcpy.readthedocs.io/en/latest/topics/get-started.html#installation

# Hardware:
# - Sony RC-S380            https://www.sony.net/Products/felica/business/tech-support/
# - Card NTAG215 type 2     https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf

# def checkTag(tag_ID):
#     """
#     Checks if a tag is registered in the database and active.
#     If tag is active then activate elevator cabin
#     """

#     if tag_ID != "":
#         tagRegistered = False
#         tagActive     = False
#         print(tag_ID)
#         with open("database.csv") as csvfile:
#             data = csv.DictReader(csvfile)
#             for row in data:
#                 if row["ID"] == tag_ID:
#                     tagRegistered = True
#                     if row["Active"]:
#                         tagActive = True
#                         #Welcome row["User"], led green, activate button panel
#                     else:
#                         #led red
# Website that will be pushed to phone when tapped
phone_website = "https://www.instagram.com/laygond/"

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

        # Push website to phone otherwise end attempt
        global started
        started = time.time()
        clf.connect(llcp={'on-connect':llcp_connected, 'lto':250, 'role':'initiator'}, terminate=immediately) 
    
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        pass
    

