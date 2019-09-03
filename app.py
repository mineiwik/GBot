####################################
#######         GBot         #######
#######      by mineiwik     #######
#######     Version: 0.1     #######
####################################

import argparse
import datetime
import gon

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-t', action='store', type=int, required=True, help='Type of generated object -> '
                                                                           '1: n-Gon; 0: exit')
args = my_parser.parse_args()

t = args.t
g_code = None
now = str(datetime.datetime.utcnow()).replace(" ", "-").replace(":", "-").split(".")[0]

if t == 1:
    height = int(input("Height in mm:\n"))
    corners = int(input("Amount of corners:\n"))
    feed = int(input("feed rate in mm/min: [800]\n") or 800)
    g_code = gon.generate_code(height, corners, feed)
else:
    exit()

file_name = "output/gcode_" + now + ".gcode"

with open(file_name, "wb") as f:
    f.write(g_code)

exit()