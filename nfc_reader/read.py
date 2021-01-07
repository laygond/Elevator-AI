import csv
import nfc
import ndef

# Tag: A card or phone is considered an NFC tag 

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

# NFC Reader must be given access rights before running code as mentioned:
# https://nfcpy.readthedocs.io/en/latest/topics/get-started.html#installation

# Verify Reader is available
clf = nfc.ContactlessFrontend()
sony_RCS380 = 'usb:054c:06c1'       # Product and Vendor ID
print(clf.open(sony_RCS380))

# Check tag's type of communication(target) and ID 
from nfc.clf import RemoteTarget
target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
print(target)
# tag = nfc.tag.activate(clf, target)
# print(tag)

# Check tag ID (preferred method)
tag = clf.connect(rdwr={'on-connect': lambda tag: False})
print(tag)

ho = clf.connect(llcp={}) # tap with phone
print(ho)

# # Write to tag
# uri, title = 'http://nfcpy.org', 'nfcpy project'
# tag.ndef.records = [ndef.SmartposterRecord(uri, title)]

# Read from tag
for record in tag.ndef.records:
    print(record)


# record = tag.ndef.records[0]
# print(record.type)
# print(record.uri)
