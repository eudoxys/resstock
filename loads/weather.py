"""Weather data accessor

Access the weather corresponding to the load data.

Example:

    Weather("CA","Alameda")

"""

import os
import datetime as dt
import pytz
import pandas as pd
from fips.counties import County
from fips.states import State

class Weather(pd.DataFrame):
    """Weather data frame implementation"""
    CACHEDIR = None

    def __init__(self,
        state:str,
        county:str,
        ):
        """Construct weather data frame for a county

        - `state`: specify the state abbreviation (required)

        - `county`: specify the county name (required)
        """
        if self.CACHEDIR is None:
            self.CACHEDIR = os.path.join(os.path.dirname(__file__),".cache")
        os.makedirs(self.CACHEDIR,exist_ok=True)

        file = os.path.join(self.CACHEDIR,f"weather_{state}_{county}.csv.gz")
        if not os.path.exists(file):
            root = "https://oedi-data-lake.s3.amazonaws.com/nrel-pds-building-stock/end-use-load-profiles-for-us-building-stock/2021/comstock_amy2018_release_1/weather/amy2018"
            fips = County(ST=state,COUNTY=county).FIPS
            tzoffset = float(State(ST=state).TZOFFSET)
            url = f"{root}/G{fips[:2]}0{fips[2:]}0_2018.csv"
            data = pd.read_csv(url,
                usecols=[
                    "date_time",
                    "Dry Bulb Temperature [°C]",
                    "Relative Humidity [%]",
                    "Global Horizontal Radiation [W/m2]", 
                    "Direct Normal Radiation [W/m2]",
                    "Diffuse Horizontal Radiation [W/m2]",
                    ],
                index_col=["date_time"]
                )
            data.index = pd.DatetimeIndex(data.index,tz=pytz.UTC) - dt.timedelta(hours=tzoffset+1)
            data.index.name = "timestamp"
            data.columns = ["temperature[degF]","humidity[%]","global[W/m^2]","direct[W/m^2]","diffuse[W/m^2]"]
            data["temperature[degF]"] = data["temperature[degF]"]*9/5+32
            data["humidity[%]"] = data["humidity[%]"].round(1)
            data.to_csv(file,index=True,header=True,compression="gzip")
        else:
            data = pd.read_csv(file,
                index_col=["timestamp"],
                parse_dates=["timestamp"],
                )

        # move year-end data to beginning
        data.index = pd.DatetimeIndex([str(x).replace("2019","2018") for x in data.index])
        super().__init__(data.sort_index())

if __name__ == '__main__':
    
    print(Weather("NY","Albany"))