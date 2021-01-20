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
import pandas as pd
import time
import argparse
import os 

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Floor&Office of Group owner")
ap.add_argument("-s", "--switch", type=str, default="",
	help=" Switch State")
args = vars(ap.parse_args())

# Read csv and find row of Floor&Office
dir_path = os.path.dirname(os.path.realpath(__file__))
cvs_path = os.path.join(dir_path,'groupData.csv')
df = pd.read_csv(cvs_path)
index_row = df.index[df['PisoOficina'].str.contains(args["input"], na=False)]

# Toggle Active column on csv
if args["switch"] == 'ON':
    df.loc[index_row,'Active'] = True
    df.to_csv(cvs_path, index=False)
if args["switch"] == 'OFF':
    df.loc[index_row,'Active'] = False
    df.to_csv(cvs_path, index=False)

# Print if Group owner has more floor&offices
floorOffices = df.loc[index_row,'PisoOficina'].values[0]
if len(floorOffices) > 4: # then it has more 
    floorOffices = floorOffices.split(',')
    floorOffices.remove(args["input"])
    print(",".join([elem for elem in floorOffices]))


# TODO:
# Reading as list and then converting seems faster
# * try  a pure a list solution
# * try csv.DictReader too
# https://stackoverflow.com/questions/11033590/change-specific-value-in-csv-file-via-python
# 
# start  = time.time()
# with open('groupData.csv','r') as dest_f:
#     data_iter = csv.reader(dest_f,
#                            delimiter = ',',
#                            quotechar = '"')
#     data = [data for data in data_iter]
#     df = pd.DataFrame(data)
#     print(df)
# print("[INFO] set took:", time.time()-start) 
