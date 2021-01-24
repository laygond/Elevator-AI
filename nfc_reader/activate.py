# -----------------------------
#   USAGE
# -----------------------------
# python activate.py --input 'P5O4' --switch 'ON'
#
# DESCRIPTION:
# This script is run in response to a change of state in any of the ON/OFF switches from the
# Openhab sitemap. For the "groupData.csv" file, sets to True or Flase the 'Active' field of 
# the row who lives in the given input floor&office, e.g., P5O4. If this row owns 
# several floor&offices then prints the remaining floor&offices so that OpenHab can turn
# ON/OFF the remaining switches. 
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
from tempfile import NamedTemporaryFile
import shutil
import time
import argparse
import os, sys 

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Floor&Office of Group owner")
ap.add_argument("-s", "--switch", type=str, default="",
	help=" Switch State")
args = vars(ap.parse_args())

# Initiate csv reader and writer
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path,'groupData.csv')
f = open(csv_path)
reader = csv.DictReader(f)
tempfile = NamedTemporaryFile(mode='w', delete=False)
writer = csv.DictWriter(tempfile, fieldnames=reader.fieldnames)

# Read and Write per row
writer.writeheader()
for row in reader:
    # Find row of Floor&Office
    if args["input"] in row["PisoOficina"]:
        # Print if Group owner has more floor&offices
        floorOffices = row['PisoOficina']
        if len(floorOffices) > 4: # then it has more 
            floorOffices = floorOffices.split(',')
            floorOffices.remove(args["input"])
            print(",".join([elem for elem in floorOffices]))
        # Toggle Active column on csv
        if args["switch"] == 'ON':
            row["Active"] = True               
        if args["switch"] == 'OFF':
            row["Active"] = False 
    # Write row
    writer.writerow(row)

# Rewrite csv once done with changes
shutil.move(tempfile.name, csv_path)