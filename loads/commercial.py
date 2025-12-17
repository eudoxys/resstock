"""Commercial building load model"""

import pandas as pd

from fips.states import States
from fips.counties import Counties
from loads.units import Units
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

            - `collect`: specify how COMstock columns are collected

            - `year`: specify the year on which the number of housing units is
              based (default most recent in `Units()`)

        This class compiles the building type data for a county by collecting
        COMstock columns, scaling by the number of housing units in that year,
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
        for btype in COMstock.BUILDING_TYPES:
            bdata = COMstock(
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

        # scale by number of commercial units and calculate fractional loads
        actual_units = Units(state=state,county=county,year=year)

        for btype in COMstock.BUILDING_TYPES:

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

        super().__init__(data[sorted(data.columns)])

    @classmethod
    def makeargs(cls,**kwargs):
        """Return dict of accepted kwargs by this class constructor"""
        return {x:y for x,y in kwargs.items()
            if x in cls.__init__.__annotations__}

if __name__ == '__main__':

    pd.options.display.width = None
    pd.options.display.max_columns = None

    print(Commercial(state="CA",county="Alameda"))
