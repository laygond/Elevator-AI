# -----------------------------
#   USAGE
# -----------------------------
# python show_active_switches.py 
#
# DESCRIPTION:
# Prints floor&Offices that are considered Active based on 'groupData.csv' 
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# COPYRIGHT:
# Code may only be distributed through http://www.laygond.com any other methods
# of obtaining or distributing are prohibited
# Copyright (c) 2020-2021
# ------------------------------

# Import the necessary packages
import csv
import os

# Read csv
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path,'groupData.csv')
f = open(csv_path)
data = csv.DictReader(f)

# Print active
floorOffices = ""
for row in data:
    if row["Active"] == 'True':
        floorOffices = ",".join([floorOffices,row["PisoOficina"]])
print(floorOffices[1:])