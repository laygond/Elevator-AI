# -----------------------------
#   USAGE
# -----------------------------
# python borrar.py --input 'P5O4' --uuid 'fourteencharid'
#
# DESCRIPTION:
# Deletes the input UUID associated with the input floor&office as
# specified in 'groupData.csv'. This script is run in response to
# clicking on button 'BORRAR' under 'NFC Last ID' on Openhab's sitemap.
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
import pandas as pd
import argparse
import os 

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Floor&Office of Group owner")
ap.add_argument("-tag", "--uuid", type=str, default="",
	help=" uuid from NFC tag")
args = vars(ap.parse_args())

# Read csv 
dir_path = os.path.dirname(os.path.realpath(__file__))
cvs_path = os.path.join(dir_path,'groupData.csv')
df = pd.read_csv(cvs_path)


# Delete UUID
if args['input'] != "" and args['uuid'] != "":
    # Verify if uuid exists
    index_row_uuid = df.index[df['UUID'].str.contains(args["uuid"], na=False)]
    if len(index_row_uuid) != 0:  #row found
        if args["input"] in df.loc[index_row_uuid,'PisoOficina'].values[0]:  
            # remove input uuid 
            uuid_values = df.loc[index_row_uuid,'UUID'].values[0].split(',')
            uuid_values.remove(args["uuid"])
            df.loc[index_row_uuid,'UUID'] = ",".join([elem for elem in uuid_values])
            # Write updates to csv
            df.to_csv(cvs_path, index=False)
            print("El uuid ha sido borrado con exito!\nDa click en VER.")
        else:
            print('Este piso & oficina no esta relacionado a este uuid. Este uuid esta registrado bajo el propietario de los siguientes pisos:\n'+
               df.loc[index_row_uuid,'PisoOficina'].values[0] +
               '\nPara borrarlo ingrese alguno de los pisos antes mencionados.'
                )
    else:
        print("Este uuid no existe bajo ningun piso & oficina. Si desea agregarlo da click en AGREGAR")
else:
    print("[INFO] This script requires an input Floor&Office and a uuid")