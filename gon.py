####################################
#######       GBot.gon       #######
#######      by mineiwik     #######
#######     Version: 1.0     #######
####################################

import datetime
from math import sin, cos, pi
import io


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0.000000


class Command:
    def __init__(self, command, props):
        space = ""
        if props != "":
            space = " "
        self.command = command + space + props + '\n'


class Props:
    def __init__(self, x, y, z):
        self.x = "X" + str('%06.6f' % x)
        self.y = " Y" + str('%06.6f' % y)
        self.z = " Z" + str('%06.6f' % z)
        self.props = self.x + self.y + self.z


def generate_code(height, corners, feed):
    date = datetime.datetime.now()
    option = 0

    f = io.StringIO()
    g_start = ["%\n", "M3 S1000\n", "G21\n"]  # Start Gcode program, turn on air pump, all units in mm
    f.writelines(g_start)

    coordinates = []

    if option == 0:
        size = height  # in mm
        points = corners  # number of corners
        speed = feed  # in mm/min
        angle = 360 / points
        radius = size / 2
        inner = int(radius / 10) + 1

        for i in range(0, inner):
            for j in range(0, points + 1):
                x = round(sin(((angle * j) / 360) * 2 * pi) * (radius - i * 10), 6)
                y = round(cos(((angle * j) / 360) * 2 * pi) * (radius - i * 10), 6)
                coordinates.append(Coordinate(x, y))
            if i < (inner - 1):
                coordinates.append('-')
            else:
                coordinates.append('end')

        codes = []
        for i in range(0, len(coordinates)):
            if i == 0:
                props = Props(coordinates[i].x, coordinates[i].y, 0.0)
                command = Command("G00", props.props)
                codes.append(command.command)
                codes.append('M5\n')
            elif i == 1:
                props = Props(coordinates[i].x, coordinates[i].y, 0.0)
                command = Command("G01", props.props + " F" + str('%06.6f' % speed))
                codes.append(command.command)
            elif coordinates[i] == '-':
                codes.append('M3 S1000\n')
            elif coordinates[i - 1] == '-':
                props = Props(coordinates[i].x, coordinates[i].y, 0.0)
                command = Command("G00", props.props)
                codes.append(command.command)
                codes.append('M5\n')
            elif coordinates[i] == 'end':
                codes.append('M3 S1000\n')
            else:
                props = Props(coordinates[i].x, coordinates[i].y, 0.0)
                command = Command("G01", props.props)
                codes.append(command.command)

        f.writelines(codes)

    g_end = ["G00 X0.0000 Y0.0000 Z0.0000\n", "M2\n", "%\n"]
    f.writelines(g_end)

    encoded = f.getvalue().encode()

    f.close()

    # return generated G-code as bytes
    return encoded

