"""Electric load data processor

Syntax: `loads [-h] [-y YEAR] [-o OUTPUT] [--building_type BUILDING_TYPE]
[--format {csv,gzip,zip,xlsx}] [--precision PRECISION] [--warning] [--debug] 
state county {residential,commercial,industrial,agricultural,public,weather}`

Positional arguments:

- `state`

- `county`

- `{residential,commercial,industrial,agricultural,public,weather}`O

Options:

-  `-h`, `--help`           show this help message and exit

- `-y`, `--year YEAR`       set load model year

- `-o`, `--output OUTPUT`   set output file name

- `--building_type BUILDING_TYPE`
                            access raw building type stock data

- `--format {csv,gzip,zip,xlsx}`
                            specify output format

- `--precision PRECISION`
                            specify output precision

- `--warning`.              enable warning messages from python

- `--debug`                 enable debug traceback on exceptions

See https://www.eudoxys.com/loads for documentation.

Example:

    loads CA Alameda residential
"""
from loads.cli import main
from loads.resstock import RESstock
from loads.residential import Residential
from loads.comstock import COMstock
from loads.units import Units
from loads.floorarea import Floorarea
from loads.industry import Industry
from loads.agriculture import Agriculture
from loads.weather import Weather
