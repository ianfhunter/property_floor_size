#! /usr/bin/env python3
from functools import reduce
import argparse
import os
import re


def define_and_parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help = "file containing the text to convert")
    parser.add_argument('-v', action='store_true', help="Verbose")

    return parser.parse_args()

def prod(x):
    return reduce(lambda a, b: a * b, x, 1)

class Area():
    def __init__(self, distances):
        self.value = prod([d.value for d in distances])

    def add(self, other):
        self.value += other.value

    def __str__(self):
        return str(self.value)

class Distance():
    def __init__(self, metres):
        self.value = metres

class ImperialDistance(Distance):
    def __init__(self, feet, inches):
        inches = feet*12 + inches
        metric = inches / 39.37
        super().__init__(metric)


def extract_measurement(line, verbose):
    dimensions = re.split(r"[xX]", line)
    sides = []
    for d in dimensions:
        if re.findall(r"[0-9]+\.?[0-9]*[mM]", d) != []:
            # Parse Metres
            metres = re.findall(r"[0-9]+\.?[0-9]*[mM]", d)[0]
            metres, centimeters = metres.split(".")
            metres = int(metres.replace("m", ""))
            centimeters = int(centimeters.replace("m", ""))
            centimeters = centimeters * pow(10, -len(str(centimeters)))
            if verbose:
                print(metres, "metres", centimeters, "centimeters")
            sides.append(Distance(metres+centimeters))

        elif "\'" in d and "\"" in d:
            # Parse Feet
            feet = re.findall(r"[0-9]+\'", d)[0]
            inches = re.findall(r"[0-9]+\"", d)[0]
            feet = int(''.join([s for s in feet if s.isdigit()]))
            inches = int(''.join([s for s in inches if s.isdigit()]))
            if verbose:
                print(feet, "Feet", inches, "Inches")
            sides.append(ImperialDistance(feet, inches))

    if sides != []:
        if verbose:
            print("Sides:", [s.value for s in sides])
        return Area(sides)
    else:
        return None

def cleanup(line):
    line = line.replace("\n","")
    line = line.replace("\s","")
    if line == "":
        return None
    else:
        return line


def command(args):
    f = args.file
    f = os.path.expanduser(f)
    f = os.path.abspath(f)

    fc = open(f, "r")
    total_area = Area([])
    for line in fc.readlines():
        line = cleanup(line)
        if line is None:
            continue
        print(line)
        room_area = extract_measurement(line, args.v)
        if room_area is not None:
            if args.v:
                print("Area:", room_area.value)
            total_area.add(room_area)

    print("Total Area:", total_area)


def main():
    args = define_and_parse_args()
    command(args)

if __name__ == "__main__":
    main()