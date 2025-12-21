[![validate](https://github.com/eudoxys/loads/actions/workflows/validate.yaml/badge.svg)](https://github.com/eudoxys/loads/actions/workflows/validate.yaml)

Electric loads data accessor and multi-sector load data tool

# Documentation

See https://www.eudoxys.com/loads

# Installation

    pip install git+https://github.com/eudoxys/loads

# Examples

## Command line

Get the Alameda county California residential load data

    loads CA Alameda residential

Outputs

                               elec_baseload_MW  elec_cooling_MW  elec_dg_MW  elec_heating_MW  elec_net_MW  elec_total_MW  nonelec_baseload_MW  nonelec_cooling_MW  nonelec_heating_MW  nonelec_total_MW
    timestamp                                                                                                                                                                                           
    2018-01-01 00:00:00+00:00            45.085            1.109      -1.053            1.772       46.913         47.966               12.102                 0.0              34.367            46.469
    2018-01-01 01:00:00+00:00            52.150            0.853       0.000            2.032       55.035         55.035               15.438                 0.0              40.053            55.491
    2018-01-01 02:00:00+00:00            58.137            0.531       0.000            3.120       61.789         61.789               16.681                 0.0              49.935            66.615
    2018-01-01 03:00:00+00:00            55.909            0.458       0.000            4.672       61.039         61.039               11.900                 0.0              64.547            76.447
    2018-01-01 04:00:00+00:00            52.824            0.342       0.000            6.428       59.594         59.594               10.311                 0.0              78.394            88.705
    ...
    2018-12-31 19:00:00+00:00            41.082            0.494      -6.454            5.576       40.697         47.151               11.204                 0.0              67.516            78.719
    2018-12-31 20:00:00+00:00            41.320            0.725      -6.780            4.226       39.490         46.271               11.824                 0.0              53.965            65.789
    2018-12-31 21:00:00+00:00            39.150            0.843      -6.397            3.124       36.719         43.116                9.804                 0.0              44.813            54.617
    2018-12-31 22:00:00+00:00            37.711            1.033      -5.342            2.649       36.051         41.393                7.904                 0.0              38.068            45.972
    2018-12-31 23:00:00+00:00            38.226            1.382      -3.725            1.664       37.548         41.272                8.399                 0.0              30.819            39.218

## Python code

Get the COMstock data frame for medium office buildings in Alameda County CA.

    from loads import COMstock
    print(COMstock(state="CA",county="Alameda",building_type="CMO"))

Outputs

Get the residential building loads data frame for Alameda County CA.

    from loads import Residential
    print(Residential(state="CA",county="Alameda"))

Outputs

# Caveat

- Although a data cache is used extensively to avoid multiple/slow queries, the
  processing of this large amount of data can be very time-consuming.

- Some COMstock and RESstock building types have no data in some counties. In
  such cases, a warning is output and a zero dataframe is constructed.
