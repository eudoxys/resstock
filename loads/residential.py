"""Residential building load model"""

import pandas as pd

from fips.states import States
from fips.counties import Counties
from loads.units import Units
from loads.resstock import RESstock

class Residential(pd.DataFrame):
    """Residential building data frame class

    The `Residential` class is a data frame that contains the collected
    building loads for each residential building types, aggregated by load
    category, i.e., `baseload`,`cooling`, `heating`, `dg`, and `total` for
    both electric and non-electric loads.  Values are delivered both in MW.
    """
    COLLECT = {
            "elec_baseload": [
                "elec_bathfan",
                "elec_ceilingfan",
                "elec_dryer",
                "elec_washer",
                "elec_cooking",
                "elec_dishwasher",
                "elec_holidaylight",
                "elec_extlighting",
                "elec_extrarefrigerator",
                "elec_freezer",
                "elec_garagelighting",
                "elec_hottubheater",
                "elec_hottubpump",
                "elec_housefan",
                "elec_interiorlighting",
                "elec_plugs",
                "elec_poolheater",
                "elec_poolpump",
                "elec_rangefan",
                "elec_recircpump",
                "elec_refrigerator",
                "elec_vehicle",
                "elec_watersystems",
                "elec_wellpump",
                ],
            "elec_cooling": [
                "elec_cooling",
                "elec_coolingfan",
                "elec_coolingpump",
                ],
            "elec_heating": [
                "elec_heating",
                "elec_heatingfan",
                "elec_heatingsupplement",
                "elec_heatingpump",
                ],
            "elec_dg":[
                "elec_pv",
                ],
            "elec_total": [
                "elec_total",
                ],
            "nonelec_baseload": [
                "oil_watersystems",
                "gas_dryer",
                "gas_cooking",
                "gas_grill",
                "gas_hottubheater",
                "gas_lighting",
                "gas_poolheater",
                "lng_dryer",
                "lng_range",
                "lng_watersystems",
                ],
            "nonelec_cooling": [
                ],
            "nonelec_heating": [
                "oil_heating",
                "gas_fireplace",
                "gas_heating",
                "gas_watersystems",
                "lng_heating",
                "wood_heating",
                ],
            "nonelec_dg": [
                ],
            "nonelec_total": [
                "oil_total",
                "gas_total",
                "lng_total",
                "wood_total",
                ],
            }

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

        - `collect`: specify how RESstock columns are collected

        - `year`: specify the year on which the number of housing units is
          based (default most recent in `Units()`)

        This class compiles the building type data for a county by collecting
        RESstock columns, scaling by the number of housing units in that year,
        and finally computing total MW and the fraction of total of electric
        or non-electric load.
        """
        # pylint: disable=too-many-locals
        assert state in States()["ST"].values, f"{state=} is not valid"
        assert county in Counties().set_index(["ST","COUNTY"]).loc[state].index, \
            f"{state=} {county=} is not valid"

        if collect is None:
            collect = self.COLLECT
            
        units = {}
        total_units = 0.0
        data = {}

        # collect building type data
        for btype in RESstock.BUILDING_TYPES:
            bdata = RESstock(
                state=state,
                county=county,
                building_type=btype,
                freq=freq,
                )
            for aggr,columns in collect.items():
                data[f"{btype}_{aggr}_MW"] = bdata[columns].sum(axis=1) / 1e6
                units[btype] = bdata["units"].max()
                total_units += units[btype]
        data = pd.DataFrame(data)

        # prepare consolidation columns
        for ctype in collect.keys():
            data[f"{ctype}_MW"] = 0.0

        # scale by number of residential units and calculate fractional loads
        actual_units = Units(state=state,county=county,year=year)

        for btype in RESstock.BUILDING_TYPES:

            # collect building type data
            for ctype in {x.split("_",1)[0] for x in collect.keys()}:
                for kwname in [x for x in data.columns if x.startswith(f"{btype}_{ctype}_")]:
                    totname = f"{btype}_{ctype}_total_MW"
                    pu = (data[kwname] / data[totname]).fillna(0.0)
                    data[kwname] *= units[btype] / total_units * actual_units

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

if __name__ == '__main__':

    pd.options.display.width = None
    pd.options.display.max_columns = None

    print(Residential(state="CA",county="Alameda"))
