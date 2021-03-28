# -----------------------------
#   USAGE
# -----------------------------
# python agregar.py --input 'P5O4' --uuid 'fourteencharid'
#
# DESCRIPTION:
# Adds the input UUID associated with the input floor&office as
# specified in 'groupData.csv'. This script is run in response to
# clicking on button 'AGREGAR' under 'NFC Last ID' on Openhab's sitemap.
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


# Add UUID
if args['input'] != "" and args['uuid'] != "":
    # Verify if uuid is registered under another floor
    index_row_uuid = df.index[df['UUID'].str.contains(args["uuid"], na=False)]
    if len(index_row_uuid) != 0:  #row found
        print('No se puede agregar uuid duplicados. Este uuid ya esta registrado bajo el propietario de los siguientes pisos:\n'+
               df.loc[index_row_uuid,'PisoOficina'].values[0] +
               '\nAntes de agregar este uuid necesita borrarlo de alguno de los pisos antes mencionados.'
            )
    else:
        # Find row of input Floor&Office
        index_row = df.index[df['PisoOficina'].str.contains(args["input"], na=False)]
        # If row found check if uuid should be appended or new instance
        if len(index_row) != 0:  #row found
            if pd.isna(df.loc[index_row,'UUID'].values[0]):  #slot empty (new instance)
                df.loc[index_row,'UUID'] = args['uuid']
            else:
                df.loc[index_row,'UUID'] = df.loc[index_row,'UUID'].values[0] + ',' + args['uuid']        
            # Write updates to csv
            df.to_csv(cvs_path, index=False)
            print("El nuevo uuid ha sido agregado con exito!\nDa click en VER.")
        else:
            print("Este Piso & Oficina no existe en este edificio. Y en este edificio se respeta las leyes de la termodinamica. ")
else:
    print("[INFO] This script requires an input Floor&Office and a uuid")