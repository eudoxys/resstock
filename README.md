[![validate](https://github.com/eudoxys/resstock/actions/workflows/validate.yaml/badge.svg)](https://github.com/eudoxys/resstock/actions/workflows/validate.yaml)

RESstock data accessor and residential load data tool

# Documentation

See https://www.eudoxys.com/resstock

# Installation

    pip install git+https://github.com/eudoxys/resstock

# Examples

## Command line

Get the raw RESstock data

    resstock --raw CA Alameda

Save the residential load data to cSV

    resstock CA Alameda -o CA-Alameda.csv

## Python code

Get the RESstock data frame for Alameda County CA.

    from resstock import RESstock
    print(RESstock(state="CA",county="Alameda",building_type="RSFD"))

Get the residential building loads data frame for Alameda County CA.

    from resstock import Residential
    print(Residential(state="CA",county="Alameda"))
