"""Commercial building load data accessor


The commercial load data frame collects and consolidates `COMstock` data. Floor areas are
obtained from `Floorarea` data to scale loads for the specified year.

Example:

To get the commercial building load data for Alameda County CA, use the following command

    from loads import Commercial
    print(Commercial(state="CA",county="Alameda"))

which outputs the following

                               elec_baseload_MW  elec_cooling_MW  elec_dg_MW  elec_heating_MW  elec_net_MW  elec_total_MW  nonelec_baseload_MW  nonelec_cooling_MW  nonelec_heating_MW  nonelec_total_MW
    2018-01-01 00:00:00+00:00          6.288318         0.640525         0.0         0.285756     7.214598       7.214598             1.953411            0.004891            0.012407          1.970713
    2018-01-01 01:00:00+00:00          6.690304         0.260410         0.0         0.436785     7.387499       7.387499             2.756313            0.003410            0.015294          2.775018
    2018-01-01 02:00:00+00:00          6.362257         0.148981         0.0         0.610040     7.121268       7.121268             3.562602            0.002878            0.021380          3.586859
    2018-01-01 03:00:00+00:00          6.157291         0.099646         0.0         0.754850     7.011784       7.011784             4.204279            0.003071            0.030086          4.237439
    2018-01-01 04:00:00+00:00          6.043443         0.081104         0.0         0.839113     6.963656       6.963656             4.642662            0.002945            0.036228          4.681834
    ...                                     ...              ...         ...              ...          ...            ...                  ...                 ...                 ...               ...
    2018-12-31 19:00:00+00:00          7.498333         0.791352         0.0         0.448009     8.737698       8.737698             2.880670            0.013928            0.029873          2.924475
    2018-12-31 20:00:00+00:00          7.660632         0.905800         0.0         0.327204     8.893635       8.893635             2.211225            0.016087            0.021963          2.249275
    2018-12-31 21:00:00+00:00          7.640507         1.024863         0.0         0.233167     8.898534       8.898534             1.722267            0.014301            0.016998          1.753567
    2018-12-31 22:00:00+00:00          7.358111         1.112202         0.0         0.199655     8.669972       8.669972             1.573820            0.012716            0.013526          1.600068
    2018-12-31 23:00:00+00:00          6.819952         1.124350         0.0         0.203216     8.147512       8.147512             1.585527            0.009863            0.011157          1.606544

    [8760 rows x 10 columns]
"""

import pandas as pd

from fips.states import States
from fips.counties import Counties
from loads.floorarea import Floorarea
from loads.comstock import COMstock

class Commercial(pd.DataFrame):
    """Commercial building data frame class

    The `Commercial` class is a data frame that contains the collected
    building loads for each commercial building types, aggregated by load
    category, i.e., `baseload`,`cooling`, `heating`, `dg`, and `total` for
    both electric and non-electric loads.  Values are delivered both in MW.
    """
    COLLECT = {
            "elec_baseload": [
                "elec_exteriorlights",
                "elec_fans",
                "elec_heatrejection",
                "elec_equipment",
                "elec_interiorlights",
                "elec_pumps",
                "elec_refrigeration",
                "elec_watersystems",
                ],
            "elec_cooling": [
                "elec_cooling",
                ],
            "elec_heating": [
                "elec_heating",
                "elec_heatrecovery",
                ],
            "elec_dg":[
                ],
            "elec_total": [
                "elec_total",
                ],
            "nonelec_baseload": [
                "district_hotwater",
                "gas_heating",
                "gas_equipment",
                "gas_watersystems",
                "other_watersystems",
                ],
            "nonelec_cooling": [
                "district_cooling",
                ],
            "nonelec_heating": [
                "other_heating",
                "district_heating",
                ],
            "nonelec_dg": [
                ],
            "nonelec_total": [
                "other_total",
                "gas_total",
                "district_totalcooling",
                "district_totalheating",
                ],
            }
    """Mapping of COMstock data columns to Commercial data columns"""

    def __init__(self,
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        state:str,
        county:str,
        freq:str="1h",
        collect=None,
        year:int=None,
        ):
        """Construct building types data frame

        Arguments:

        - `state`: specify the state abbreviation (required)

        - `county`: specify the county name (required)

        - `freq`: specify the data sampling frequency (default is "1h"")

        - `collect`: specify how COMstock columns are collected (default is `COLLECT`)

        - `year`: specify the year on which the floor area is based
          (default most recent in `Floorarea()`)

        This class compiles the building type data for a county by collecting
        COMstock columns, scaling by the floor area in that year, and finally
        computing total electric and non-electric loads in MW.
        """
        # pylint: disable=too-many-locals
        assert state in States()["ST"].values, f"{state=} is not valid"
        assert county in Counties().set_index(["ST","COUNTY"]).loc[state].index, \
            f"{state=} {county=} is not valid"

        if collect is None:
            collect = self.COLLECT
            
        floorarea = {}
        total_area = 0.0
        data = {}

        # split floor areas by building type
        actual_areas = Floorarea(state=state,county=county,year=year).set_index("BUILDING_TYPE").sort_index()
        split_areas = {"BUILDING_TYPE":[],"FLOORAREA":[],"SPLITS":[],"FRACTION":[]}
        actual_areas_sum = actual_areas.FLOORAREA.sum()
        for bts,area in list(actual_areas.iterrows()):
            for bt in bts.split("|"):
                split_areas["BUILDING_TYPE"].append(bt if bt else "OTH")
                split_areas["FLOORAREA"].append(area.FLOORAREA / len(bts.split("|")))
                split_areas["SPLITS"].append(bts)
                split_areas["FRACTION"].append(area.FLOORAREA/actual_areas_sum)
        split_areas = pd.DataFrame(split_areas).set_index("BUILDING_TYPE")

        # collect building type data
        for btype in COMstock.BUILDING_TYPES:
            bdata = COMstock(
                state=state,
                county=county,
                building_type=btype,
                freq=freq,
                )
            for aggr,columns in collect.items():
                data[f"{btype}_{aggr}_MW"] = bdata[columns].sum(axis=1) / 1e6
                floorarea[btype] = bdata["floor_area"].max()
                total_area += floorarea[btype]
        data = pd.DataFrame(data)

        # prepare consolidation columns
        for ctype in collect.keys():
            data[f"{ctype}_MW"] = 0.0

        # collect and consolidate data
        for btype in COMstock.BUILDING_TYPES:

            # collect building type data
            for ctype in {x.split("_",1)[0] for x in collect.keys()}:
                for kwname in [x for x in data.columns if x.startswith(f"{btype}_{ctype}_")]:
                    totname = f"{btype}_{ctype}_total_MW"
                    pu = (data[kwname] / data[totname]).fillna(0.0)
                    data[kwname] *= floorarea[btype] / total_area * split_areas.loc[btype].FLOORAREA

            # consolidate building type data
            for ctype in collect.keys():
                data[f"{ctype}_MW"] += data[f"{btype}_{ctype}_MW"]
                data.drop(f"{btype}_{ctype}_MW",axis=1,inplace=True)

        # update net total with DG
        data["elec_net_MW"] = data["elec_total_MW"] + data["elec_dg_MW"]
        data.drop("nonelec_dg_MW",axis=1,inplace=True)

        # move year-end data to beginning
        data.index = pd.DatetimeIndex([str(x).replace("2019","2018") for x in data.index])
        super().__init__(data.sort_index()[sorted(data.columns)])

    @classmethod
    def makeargs(cls,**kwargs):
        """Return dict of accepted kwargs by this class constructor"""
        return {x:y for x,y in kwargs.items()
            if x in cls.__init__.__annotations__}
