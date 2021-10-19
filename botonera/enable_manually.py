# -----------------------------
#   USAGE
# -----------------------------
# python enable_manually.py --input 'True'
#
# DESCRIPTION:
# This script is used for debugging.
# Set enable pickle file to True or False manually from command line.
# Regardless of input it always prints the state of the enable file.
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
# ------------------------------

# Import necessary packages
import argparse
import pickle

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Button to Press in Elevator")
args = vars(ap.parse_args())

# Helper Function
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Modify enable file 
if args["input"]:
    f = open('enable','wb')
    botonera_enabled_through_tag= str2bool(args["input"])
    pickle.dump(botonera_enabled_through_tag,f)
    f.close()

# Print enable file
f = open('enable','rb')
botonera_enabled_through_tag = pickle.load(f)
f.close()
print(botonera_enabled_through_tag)