"""Housing units

Example:

The number of housing units in Alameda County CA in 2020 is obtained with the code

    from loads.units import Units
    print(Units("CA","Alameda",2020))

which gives the following output

    623350.0

See https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-housing-units.html

"""

import os
import warnings
import socket

import pandas as pd

from fips.states import State

# pylint: disable=redefined-outer-name
class Units(float):
    """Class to contain the number of residential units in a county for a year"""
    CACHEDIR = None
    """Cache folder path (`None` is package source folder)"""

    def __new__(cls,
        state:str,
        county:str=None,
        year:str|int=None,
        ):
        """Load housing units from Census Bureau

        Arguments:

        - `state`: state for which to read data

        - `county`: county for which to read data (default entire state)

        - `year`: year for which to read data (default most recent)
        """

        if cls.CACHEDIR is None:
            cls.CACHEDIR = os.path.join(os.path.dirname(__file__),".cache")
        os.makedirs(cls.CACHEDIR,exist_ok=True)

        cache = os.path.join(cls.CACHEDIR,f"{state}_housing_units.csv")

        if not os.path.exists(cache):

            root = "https://www2.census.gov/programs-surveys/popest/tables/2020-2024/housing/totals"
            info = State(ST=state)
            name = f"CO-EST2024-HU-{info.FIPS}"
            url = f"{root}/{name}.xlsx"
            old_timeout = socket.getdefaulttimeout()
            retry = 5
            while retry > 0:
                try:
                    socket.setdefaulttimeout(5)
                    data = pd.read_excel(url,
                        sheet_name=name,
                        skiprows=2,
                        header=1,
                        index_col=[0],
                        usecols=[0,2,3,4,5,6],
                        ).dropna()
                    break
                except socket.timeout:
                    retry -= 1
                finally:
                    socket.setdefaulttimeout(old_timeout)
            if retry == 0:
                raise socket.timeout(f"maximum retries exceeded getting {url=}")
            data.to_csv(cache,index=True,header=True)

        else:

            data = pd.read_csv(cache,index_col=[0])

        if year is None:
            year = data.columns[-1]
        else:
            year = int(year)
        assert year in [int(x) for x in data.columns], f"{year=} is not valid, must be one of {data.columns}"

        if county is None:
            row = data.index
        else:
            row = [x for x in data.index if x.startswith(f".{county}")]

        result = data.loc[row,str(year)].values
        if len(result) != 1:
            warnings.warn(f"Units({state=},{county=},{year=}) "\
                f"did not result in a single value ({result=})")
            return float('nan')
        return result[0]
