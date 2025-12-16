"""Housing units

See https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-housing-units.html

"""

import os
import sys
import socket
import pandas as pd
from fips.states import State, States
from fips.counties import Counties

class Units(float):

    CACHEDIR = None

    def __new__(self,
        state:str,
        county:str=None,
        year:str=None,
        ):
        """Load housing units from Census Bureau"""

        if self.CACHEDIR is None:
            self.CACHEDIR = os.path.join(os.path.dirname(__file__),".cache")
        os.makedirs(self.CACHEDIR,exist_ok=True)
        
        cache = os.path.join(self.CACHEDIR,f"{state}_housing_units.csv")

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
        assert year in data.columns, f"{year=} is not valid"

        if county is None:
            row = data.index
        else:
            row = [x for x in data.index if x.startswith(f".{county}")]

        result = data.loc[row,year].values
        if len(result) == 1:
            return result[0]
        else:
            return float('nan')

if __name__ == '__main__':

    pd.options.display.width = None
    pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    
    for _,state in States().iterrows():
        print("***",state.ST,f"({state.FIPS})","***",flush=True)
        for _,county in Counties(state.ST).iterrows():
            try:
                print(county.COUNTY,f"{state.ST}:",Units(state.ST,county.COUNTY),flush=True)
            except Exception as err:
                print(f"ERROR [{county.COUNTY} {state.ST}]: {err}",flush=True)