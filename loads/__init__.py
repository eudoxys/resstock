"""RESstock command line processor

Usage:

    resstock [-h] [-o OUTPUT] FORM

Exapmle:

    resstock CA Alameda
"""
from resstock.cli import main
from resstock.resstock import RESstock, Residential
from resstock.units import Units
