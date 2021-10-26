# -----------------------------
#   USAGE
# -----------------------------
# python ver.py --input 'P5O4' 
#
# DESCRIPTION:
# Prints all the UUID associated with the input floor&office as
# specified in 'groupData.csv'. This script is run in response to
# clicking on button 'VER' under 'NFC Last ID' on Openhab's sitemap.
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# COPYRIGHT:
# Code may only be distributed through
# http://www.laygond.com or https://github.com/laygond
# any other methods of obtaining or distributing are prohibited
# Copyright (c) 2020-2021
# ------------------------------

# Import the necessary packages
import csv
import os
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Floor&Office of Group owner")
ap.add_argument("-tag", "--uuid", type=str, default="",
	help=" uuid from NFC tag")
args = vars(ap.parse_args())

# Set csv path point to active group
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(dir_path,'groupData.csv')

# Display data
text1 = "=== UUID TAG INFO ==="
if args['uuid'] != "":
    f = open(csv_path)
    data = csv.DictReader(f) 
    input_found = False
    for row in data:
        if args['uuid'] in row['UUID']:
            text1 = text1 \
                   +'\nActivo: '+row['Active'] \
                   +'\nUUID asociados:\n\t' \
                   +"\n\t".join(row['UUID'].split(',')) \
                   +'\nPisos & Oficinas asociados:\n\t' \
                   +"\n\t".join(row['PisoOficina'].split(',')) 
            input_found = True
            break
    if not input_found:
        text1 = text1 + "\nEste tag no esta registrado. Si desea registrarlo elegir Piso y Oficina y luego dar click en AGREGAR."
    f.seek(0)    # reset file pointer
else:
    text1 = text1 + "\nNingun uuid tag fue escaneado"

text2 = "\n\n=== PISOS & OFICINAS INFO ==="
if args['input'] != "":
    f = open(csv_path)
    data = csv.DictReader(f) 
    input_found = False
    for row in data:
        if args['input'] in row['PisoOficina']:
            text2 = text2 \
                   +'\nActivo: '+row['Active'] \
                   +'\nUUID asociados:\n\t' \
                   +"\n\t".join(row['UUID'].split(',')) \
                   +'\nPisos & Oficinas asociados:\n\t' \
                   +"\n\t".join(row['PisoOficina'].split(','))
            input_found = True
            break
    if not input_found:
        text2 = text2 +"\nEste Piso & Oficina no existe en este edificio. Y en este edificio se respeta las leyes de la termodinamica."
else:
    text2 = text2 + "\nNingun Piso & Oficina fue selecionado"

print(text1,text2)
