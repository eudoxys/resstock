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

Get the COMstock data frame for medium office buildings in Alameda County CA.

    from loads import COMstock
    print(COMstock(state="CA",county="Alameda",building_type="CMO"))

Get the residential building loads data frame for Alameda County CA.

    from loads import Residential
    print(Residential(state="CA",county="Alameda"))

# Caveat

- Although a data cache is used extensively to avoid multiple/slow queries, the
  processing of this large amount of data can be very time-consuming.

- Some COMstock and RESstock building types have no data in some counties. In
  such cases, a warning is output and a zero dataframe is constructed.
