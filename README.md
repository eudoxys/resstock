[![validate](https://github.com/eudoxys/loads/actions/workflows/validate.yaml/badge.svg)](https://github.com/eudoxys/loads/actions/workflows/validate.yaml)

Electric loads data accessor and multi-sector load data tool

# Documentation

See https://www.eudoxys.com/loads

# Installation

    pip install git+https://github.com/eudoxys/loads

# Examples

## Command line

Get the raw RESstock data

    loads --raw CA Alameda

Save the residential load data to cSV

    loads CA Alameda -o CA-Alameda.csv

## Python code

Get the RESstock data frame for Alameda County CA.

    from loads import RESstock
    print(RESstock(state="CA",county="Alameda",building_type="RSFD"))

Get the residential building loads data frame for Alameda County CA.

    from loads import Residential
    print(Residential(state="CA",county="Alameda"))
