"""RESstock data accessor"""

import os
import sys
import datetime as dt
import pytz
import urllib
import warnings
import pandas as pd
import requests
from fips.states import States
from fips.counties import Counties, County
from loads.units import Units # normal usage

def _float(s,default=0.0):
    try:
        return float(s)
    except ValueError:
        return default

class RESstock(pd.DataFrame):
    """The `RESstock` class is a Pandas data frame loaded with the RESstock
    building data.

    The data frame includes the columns specified by `COLUMNS` constant, which
    maps the RESstock data to the data frame columns. The values are given in
    average Watts per housing unit. The number of units from RESstock is
    given by the `units` column. Note that the number of units is that used
    in the RESstock model, which may not be accurately reflect the actual
    number of units in any given year.
    """
    CACHEDIR = None
    COLUMNS = {
        "out.electricity.bath_fan.energy_consumption": "elec_bathfan",
        "out.electricity.ceiling_fan.energy_consumption": "elec_ceilingfan",
        "out.electricity.clothes_dryer.energy_consumption": "elec_dryer",
        "out.electricity.clothes_washer.energy_consumption": "elec_washer",
        "out.electricity.cooking_range.energy_consumption": "elec_cooking",
        "out.electricity.cooling.energy_consumption": "elec_cooling",
        "out.electricity.dishwasher.energy_consumption": "elec_dishwasher",
        "out.electricity.ext_holiday_light.energy_consumption": "elec_holidaylight",
        "out.electricity.exterior_lighting.energy_consumption": "elec_extlighting",
        "out.electricity.extra_refrigerator.energy_consumption": "elec_extrarefrigerator",
        "out.electricity.fans_cooling.energy_consumption": "elec_coolingfan",
        "out.electricity.fans_heating.energy_consumption": "elec_heatingfan",
        "out.electricity.freezer.energy_consumption": "elec_freezer",
        "out.electricity.garage_lighting.energy_consumption": "elec_garagelighting",
        "out.electricity.heating.energy_consumption": "elec_heating",
        "out.electricity.heating_supplement.energy_consumption": "elec_heatingsupplement",
        "out.electricity.hot_tub_heater.energy_consumption": "elec_hottubheater",
        "out.electricity.hot_tub_pump.energy_consumption": "elec_hottubpump",
        "out.electricity.house_fan.energy_consumption": "elec_housefan",
        "out.electricity.interior_lighting.energy_consumption": "elec_interiorlighting",
        "out.electricity.plug_loads.energy_consumption": "elec_plugs",
        "out.electricity.pool_heater.energy_consumption": "elec_poolheater",
        "out.electricity.pool_pump.energy_consumption": "elec_poolpump",
        "out.electricity.pumps_cooling.energy_consumption": "elec_coolingpump",
        "out.electricity.pumps_heating.energy_consumption": "elec_heatingpump",
        "out.electricity.pv.energy_consumption": "elec_pv",
        "out.electricity.range_fan.energy_consumption": "elec_rangefan",
        "out.electricity.recirc_pump.energy_consumption": "elec_recircpump",
        "out.electricity.refrigerator.energy_consumption": "elec_refrigerator",
        "out.electricity.total.energy_consumption": "elec_total",
        "out.electricity.vehicle.energy_consumption": "elec_vehicle",
        "out.electricity.water_systems.energy_consumption": "elec_watersystems",
        "out.electricity.well_pump.energy_consumption": "elec_wellpump",
        "out.fuel_oil.heating.energy_consumption": "oil_heating",
        "out.fuel_oil.total.energy_consumption": "oil_total",
        "out.fuel_oil.water_systems.energy_consumption": "oil_watersystems",
        "out.natural_gas.clothes_dryer.energy_consumption": "gas_dryer",
        "out.natural_gas.cooking_range.energy_consumption": "gas_cooking",
        "out.natural_gas.fireplace.energy_consumption": "gas_fireplace",
        "out.natural_gas.grill.energy_consumption": "gas_grill",
        "out.natural_gas.heating.energy_consumption": "gas_heating",
        "out.natural_gas.hot_tub_heater.energy_consumption": "gas_hottubheater",
        "out.natural_gas.lighting.energy_consumption": "gas_lighting",
        "out.natural_gas.pool_heater.energy_consumption": "gas_poolheater",
        "out.natural_gas.total.energy_consumption": "gas_total",
        "out.natural_gas.water_systems.energy_consumption": "gas_watersystems",
        "out.propane.clothes_dryer.energy_consumption": "lng_dryer",
        "out.propane.cooking_range.energy_consumption": "lng_range",
        "out.propane.heating.energy_consumption": "lng_heating",
        "out.propane.total.energy_consumption": "lng_total",
        "out.propane.water_systems.energy_consumption": "lng_watersystems",
        "out.site_energy.total.energy_consumption": "total",
        "out.wood.heating.energy_consumption": "wood_heating",
        "out.wood.total.energy_consumption": "wood_total",
    }
    BUILDING_TYPES = {
        "RSFD": "single-family_detached",
        "RSFA": "single-family_attached",
        "RMFS": "multi-family_with_2_-_4_units",
        "RMFM": "multi-family_with_5plus_units",
        "RMH": "mobile_home",
    }
    STATES = States().values.tolist()
    def __init__(self,
        state:str,
        county:str=None,
        building_type:list[str]=None,
        freq:str|None="1h",
        ):
        """Construct a RESstock data frame

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
                "end-use-load-profiles-for-us-building-stock/2021/resstock_amy2018_release_1/timeseries_aggregates"
            btype = self.BUILDING_TYPES[building_type]
            if county is None:
                url = f"{root}/by_state/state={state.upper()}/{state.lower()}-{btype}.csv"
            else:
                fips = County(ST=state,COUNTY=county).FIPS
                url = f"{root}/by_county/state={state.upper()}/g{fips[:2]}0{fips[2:]}0-{btype}.csv"
            try:
                data = pd.read_csv(url)
            except urllib.error.HTTPError as err:
                print(f"ERROR [RESstock]: {url=}",file=sys.stderr)
                raise 
            data.to_csv(cache,compression="gzip" if cache.endswith(".gz") else None)
        
        # load data from cache
        data = pd.read_csv(cache,dtype=str,na_filter=False,low_memory=False)
        data.set_index(["timestamp"],inplace=True)
        data.index = (pd.DatetimeIndex(data.index,tz=pytz.timezone("EST")) - dt.timedelta(minutes=15)).tz_convert(pytz.UTC)

        # capture number of housing units
        units = data["units_represented"].astype(float)
        if units.min() != units.max():
            warnings.warn(f"{state=} {county=} number of units changes (using max)")
        units = units.max()

        # restructure data
        data.drop([x for x in data.columns if x not in self.COLUMNS],inplace=True,axis=1)
        data.rename({x:y for x,y in self.COLUMNS.items()},inplace=True,axis=1)
        for value in self.COLUMNS.values():
            data[value] = [_float(x)/units*1000 for x in data[value]]

        data["units"] = units

        # resample if necessary
        if freq is None:
            super().__init__(data)
        else:
            ts = data.index.diff().mean().total_seconds()/3600
            super().__init__((data/ts).resample(freq).ffill())

    @classmethod
    def makeargs(cls,**kwargs):
        """Return dict of accepted kwargs by this class constructor"""
        return {x:y for x,y in kwargs.items()
            if x in cls.__init__.__annotations__}

if __name__ == '__main__':
    
    pd.options.display.width = None
    pd.options.display.max_columns = None
    
    print(RESstock(state="CA",county="Alameda",building_type="RSFD"))

