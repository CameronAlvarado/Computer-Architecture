#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

with open(sys.argv[1], 'r') as f:
    contents = f.read()
    print(contents)

# program = open("examples/mult.ls8", "r")
# if program.mode == 'r':
#     contents = program.read()
#     print(contents)

cpu.load(contents)
cpu.run()
