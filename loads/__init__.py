"""RESstock command line processor

Usage:

    loads [-h] [-o OUTPUT] FORM

Exapmle:

    loads CA Alameda
"""
from loads.cli import main
from loads.resstock import RESstock
from loads.residential import Residential
from loads.comstock import COMstock
from loads.units import Units
from loads.floorarea import Floorarea
