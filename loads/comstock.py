"""COMstock data accessor

The `COMstock` class is a Pandas data frame loaded with the COMstock
building data.

Commercial building types are coded using three characters `C`, 
`{'L','M','S'}` (large, medium, and small), and
`{'F','H','L','O','E','R','W'}` (food, health, lodging, office,
education, retail, and warehouse). Load values are given in W/sf.

Example:

To get the large office load data for Alameda CA use the command

    print(COMstock(state="CA",building_type="CLO"))

which outputs the following

                               district_cooling  ...    floor_area
    2018-01-01 00:00:00+00:00          0.003947  ...  1.673457e+09
    2018-01-01 01:00:00+00:00          0.001914  ...  1.673457e+09
    2018-01-01 02:00:00+00:00          0.000239  ...  1.673457e+09
    2018-01-01 03:00:00+00:00          0.000000  ...  1.673457e+09
    2018-01-01 04:00:00+00:00          0.000000  ...  1.673457e+09
    ...                                     ...  ...           ...
    2018-12-31 19:00:00+00:00          0.005069  ...  1.673457e+09
    2018-12-31 20:00:00+00:00          0.004822  ...  1.673457e+09
    2018-12-31 21:00:00+00:00          0.004999  ...  1.673457e+09
    2018-12-31 22:00:00+00:00          0.006171  ...  1.673457e+09
    2018-12-31 23:00:00+00:00          0.005937  ...  1.673457e+09

    [8760 rows x 26 columns]
"""

import os
import datetime as dt
import urllib
import warnings

import pytz
import pandas as pd

from fips.counties import County

def _float(s,default=0.0):
    try:
        return float(s)
    except ValueError:
        return default

class COMstock(pd.DataFrame):
    """Construct a COMstock data frame

    The data frame includes the columns specified by `COLUMNS` constant, which
    maps the COMstock data to the data frame columns. The values are given in
    average Watts per unit floor area in square feet. The number of units
    from COMstock is given by the `floor_area` column. Note that the floor
    area is that used in the COMstock model, which may not be accurately
    reflect the actual floor area in any given year.
    """

    # pylint: disable=invalid-name,too-many-locals
    CACHEDIR = None
    """Cache folder path (`None` is package source folder)"""

    COLUMNS = {
        "out.district_cooling.cooling.energy_consumption": "district_cooling",
        "out.district_heating.heating.energy_consumption": "district_heating",
        "out.district_heating.water_systems.energy_consumption": "district_hotwater",
        "out.electricity.cooling.energy_consumption": "elec_cooling",
        "out.electricity.exterior_lighting.energy_consumption": "elec_exteriorlights",
        "out.electricity.fans.energy_consumption": "elec_fans",
        "out.electricity.heat_recovery.energy_consumption": "elec_heatrecovery",
        "out.electricity.heat_rejection.energy_consumption": "elec_heatrejection",
        "out.electricity.heating.energy_consumption": "elec_heating",
        "out.electricity.interior_equipment.energy_consumption": "elec_equipment",
        "out.electricity.interior_lighting.energy_consumption": "elec_interiorlights",
        "out.electricity.pumps.energy_consumption": "elec_pumps",
        "out.electricity.refrigeration.energy_consumption": "elec_refrigeration",
        "out.electricity.water_systems.energy_consumption": "elec_watersystems",
        "out.natural_gas.heating.energy_consumption": "gas_heating",
        "out.natural_gas.interior_equipment.energy_consumption": "gas_equipment",
        "out.natural_gas.water_systems.energy_consumption": "gas_watersystems",
        "out.district_cooling.total.energy_consumption": "district_totalcooling",
        "out.district_heating.total.energy_consumption": "district_totalheating",
        "out.electricity.total.energy_consumption": "elec_total",
        "out.natural_gas.total.energy_consumption": "gas_total",
        "out.other_fuel.heating.energy_consumption": "other_heating",
        "out.other_fuel.water_systems.energy_consumption": "other_watersystems",
        "out.other_fuel.total.energy_consumption": "other_total",
        "out.site_energy.total.energy_consumption": "total"
    }
    """Mapping of COMstock raw columns to COMstock data frame columns"""

    BUILDING_TYPES = {
        "CLF": "fullservicerestaurant",
        "CLH": "hospital",
        "CLL": "largehotel",
        "CLO": "largeoffice",
        "CSH": "outpatient",
        "CMO": "mediumoffice",
        "CSE": "primaryschool",
        "CSF": "quickservicerestaurant",
        "CSR": "retailstandalone",
        "CMR": "retailstripmall",
        "CME": "secondaryschool",
        "CSL": "smallhotel",
        "CSO": "smalloffice",
        "CMW": "warehouse",
    }
    """COMstock building type codes"""

    def __init__(self,
        state:str,
        county:str=None,
        building_type:list[str]=None,
        freq:str|None="1h",
        ):
        """Construct a COMstock data frame

        Arguments:

        - `state`: specifies the state (e.g., "CA")

        - `county`: specifies the county (e.g., "Alameda") or None for the
          entire state

        - `building_type`: specifies the building type (e.g., "house")

        - `freq`: specifies the sampling interval (None for raw sampling)
        """
        assert building_type in self.BUILDING_TYPES, \
            f"{building_type=} is not one of {self.BUILDING_TYPES}"

        if self.CACHEDIR is None:
            self.CACHEDIR = os.path.join(os.path.dirname(__file__),".cache")
        os.makedirs(self.CACHEDIR,exist_ok=True)

        # check cache
        file = f"{state}_{building_type}.csv.gz" \
            if county is None \
            else f"{state}_{county}_{building_type}.csv.gz"
        cache = os.path.join(self.CACHEDIR,file.replace(" ","-"))
        if not os.path.exists(cache):

            # download data to cache
            root = "https://oedi-data-lake.s3.amazonaws.com/nrel-pds-building-stock/" \
                "end-use-load-profiles-for-us-building-stock/2021/" \
                "comstock_amy2018_release_1/timeseries_aggregates"
            btype = self.BUILDING_TYPES[building_type]
            if county is None:
                url = f"{root}/by_state/state={state.upper()}/{state.lower()}-{btype}.csv"
            else:
                fips = County(ST=state,COUNTY=county).FIPS
                url = f"{root}/by_county/state={state.upper()}/g{fips[:2]}0{fips[2:]}0-{btype}.csv"
            try:
                data = pd.read_csv(url)
            except urllib.error.HTTPError as err:

                # download error (most likely no data in COMstock)
                warnings.warn(f"COMstock building type '{btype}' has no data ({err})")

                # create all zeros dataframe
                ndx = pd.date_range(
                    start="2018-01-01 05:00:00+00:00",
                    end="2019-01-01 04:00:00+00:00",
                    freq=freq)
                zeros = [0.0]*len(ndx)
                data = pd.DataFrame(data={x:zeros for x in self.COLUMNS},index=ndx)
                data.index.name = "timestamp"
                data.reset_index(inplace=True)
                data["floor_area_represented"] = 0.0

            data.to_csv(cache,compression="gzip" if cache.endswith(".gz") else None)

        # load data from cache
        data = pd.read_csv(cache,dtype=str,na_filter=False,low_memory=False)
        data.set_index(["timestamp"],inplace=True)
        data.index = (pd.DatetimeIndex(data.index,tz=pytz.timezone("EST")) \
            - dt.timedelta(minutes=15)).tz_convert(pytz.UTC)

        # capture number floor_area
        floor_area = data["floor_area_represented"].astype(float)
        if floor_area.min() != floor_area.max():
            warnings.warn(f"{state=} {county=} floor area changes (using max)")
        floor_area = floor_area.max()

        # restructure data
        data.drop([x for x in data.columns if x not in self.COLUMNS],inplace=True,axis=1)
        data.rename(self.COLUMNS,inplace=True,axis=1)
        for value in self.COLUMNS.values():
            data[value] = [0.0 if floor_area == 0.0
                else _float(x)/floor_area*1000 for x in data[value]]

        data["floor_area"] = floor_area

        # resample if necessary
        if not freq is None:
            ts = data.index.diff().mean().total_seconds()/3600
            data = (data/ts).resample(freq).ffill()

        # move year-end data to beginning
        data.index = pd.DatetimeIndex([str(x).replace("2019","2018") for x in data.index])
        super().__init__(data.sort_index())

    @classmethod
    def makeargs(cls,**kwargs):
        """Return dict of accepted kwargs by this class constructor"""
        return {x:y for x,y in kwargs.items()
            if x in cls.__init__.__annotations__}
