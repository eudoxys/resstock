"""RESstock data accessor

The `RESstock` class is a Pandas data frame loaded with the RESstock
building data.

Residental building types are coded using three characters `R` for
residential, `{'SA','SD','SM','LM','MH'}` for single-family attached,
single-family detached, small multi-family, large multi-family, and
mobile-home. Values are given in W/unit.

Example:

To get the detached single-family home load data for Alameda CA use the command

    print(RESstock(state="CA",county="Alameda",building_type="RSD"))

which outputs the following

                               elec_bathfan  elec_ceilingfan  elec_dryer  elec_washer  elec_cooking  elec_cooling  elec_dishwasher  elec_holidaylight  elec_extlighting  elec_extrarefrigerator  elec_coolingfan  elec_heatingfan  elec_freezer  elec_garagelighting  elec_heating  elec_heatingsupplement  elec_hottubheater  elec_hottubpump  elec_housefan  elec_interiorlighting  elec_plugs  elec_poolheater  elec_poolpump  elec_coolingpump  elec_heatingpump     elec_pv  elec_rangefan  elec_recircpump  elec_refrigerator   elec_total  elec_vehicle  elec_watersystems  elec_wellpump  oil_heating  oil_total  oil_watersystems  gas_dryer  gas_cooking  gas_fireplace  gas_grill  gas_heating  gas_hottubheater  gas_lighting  gas_poolheater    gas_total  gas_watersystems  lng_dryer  lng_range  lng_heating  lng_total  lng_watersystems        total  wood_heating  wood_total        units
    2018-01-01 00:00:00+00:00      0.591256              0.0   91.735253     4.493915     39.677425     13.872222         7.110010                0.0          9.517666               17.144892         3.398066         2.653911      6.774663             1.997502     19.154867                     0.0          20.248155        38.780987            0.0             138.807467  352.836463         2.133657      45.367184               0.0          0.001468  -30.636165       2.851943              0.0          48.158305   898.648461           0.0          24.917231       6.423954          0.0   0.000000          0.000000  46.692320   118.085683       8.052885   7.377692   132.500937         43.159902      0.853789       22.473497   856.121459        476.924753        0.0   0.000000     0.464963   8.426143          7.961180  1763.196054           0.0         0.0  1253270.056
    2018-01-01 01:00:00+00:00      0.973834              0.0   87.019281     4.140658     40.726500      9.286226         6.756403                0.0         12.934264               18.703519         2.449120         3.869390      7.390541             2.714554     22.760566                     0.0          19.605356        37.549844            0.0             212.416095  395.533762         1.326327      28.201222               0.0          0.002446   -0.000000       4.335880              0.0          52.536332  1004.793603           0.0          25.424474       8.137008          0.0   1.304679          1.304679  66.496219   163.326612      10.200321  10.798259   210.654172         41.789747      1.081466       13.970012  1061.623092        543.306284        0.0   0.000000     1.331199   7.343335          6.012136  2075.064785           0.0         0.0  1253270.056
    2018-01-01 02:00:00+00:00      1.356412              0.0   66.787795     5.372866     51.261957      4.513617        13.542147                0.0         15.374691               19.482832         1.342383         6.934026      7.698481             3.226734     37.751425                     0.0          10.927576        20.929421            0.0             296.956237  429.803301         0.749663      15.939821               0.0          0.004632   -0.000000       3.617098              0.0          54.725346  1108.727577           0.0          31.007317       9.421799          0.0   0.000000          0.000000  49.158528   200.503577      11.810898   7.713042   387.342298         23.292646      1.252223        7.896094  1266.874430        577.905124        0.0   0.000000     1.439487  27.607044         26.167558  2403.209216           0.0         0.0  1253270.056
    2018-01-01 03:00:00+00:00      1.599870              0.0   55.489281     6.329422     36.005232      3.072565        18.098011                0.0         16.350862               18.703519         0.699381        11.241075      7.390541             3.431606     60.654394                     0.0           9.802678        18.774922            0.0             305.999245  418.659560         0.461331       9.809121               0.0          0.008551   -0.000000       2.063601              0.0          52.536332  1093.182103           0.0          25.151659      10.849344          0.0   1.322840          1.322840  58.636304   130.941668      13.600428   4.694895   630.644405         20.894873      1.441954        4.859135  1551.856716        686.143054        0.0   0.000000     4.985856  15.021150         10.035294  2661.383222           0.0         0.0  1253270.056
    2018-01-01 04:00:00+00:00      1.634650              0.0   74.652869     7.248296     26.396881      1.790075        13.853606                0.0         17.327032               18.313862         0.453092        16.525459      7.236572             3.636478     88.968439                     0.0           8.195682        15.697066            0.0             256.772727  407.710209         0.230666       4.904560               0.0          0.013588   -0.000000       0.811528              0.0          51.441825  1070.809428           0.0          35.431148      11.563116          0.0   1.305379          1.305379  79.616994   106.077962      14.495193   2.951077   906.260983         17.469484      1.536820        2.429567  1816.425429        685.587348        0.0   0.000000     7.583644  14.092351          6.508707  2902.633238           0.0         0.0  1253270.056
    ...                                 ...              ...         ...          ...           ...           ...              ...                ...               ...                     ...              ...              ...           ...                  ...           ...                     ...                ...              ...            ...                    ...         ...              ...            ...               ...               ...         ...            ...              ...                ...          ...           ...                ...            ...          ...        ...               ...        ...          ...            ...        ...          ...               ...           ...             ...          ...               ...        ...        ...          ...        ...               ...          ...           ...         ...          ...
    2018-12-31 19:00:00+00:00      0.324611              0.0   85.749190     5.270266     25.233848      3.250146         3.181940                0.0          6.101068               15.586265         0.763981        12.555710      6.158785             1.280450     67.907268                     0.0           2.249795         4.308999            0.0              94.998712  321.573053         6.977634     148.362953               0.0          0.012477 -187.693435       1.623057              0.0          43.780277   891.981455           0.0          30.020071       4.710899          0.0   1.305163          1.305163  85.687833    72.793389       5.905449   3.085217   675.585251          4.795545      0.626112       73.494411  1634.916820        712.943614        0.0   0.000000     4.726364  21.388418         16.662053  2549.592499           0.0         0.0  1253270.056
    2018-12-31 20:00:00+00:00      0.475324              0.0   64.666200     5.023743     31.640323      7.412980         5.325994                0.0          5.857025               16.365579         1.506082         9.036830      6.466724             1.229232     48.037234                     0.0           2.249795         4.308999            0.0              90.325640  324.885121         6.919967     147.136812               0.0          0.009260 -197.184400       1.692616              0.0          45.969291   862.903812           0.0          31.794897       4.568145          0.0   0.000000          0.000000  67.762743    98.032746       5.726496   2.816937   501.342206          4.795545      0.607139       72.887019  1328.835915        574.865083        0.0   2.466962     2.990363  13.087194          7.629869  2204.827333           0.0         0.0  1253270.056
    2018-12-31 21:00:00+00:00      0.486917              0.0   88.347619     4.384204     24.067991      9.498124         2.762858                0.0          6.833196               16.365579         1.861888         6.371460      6.466724             1.434104     33.250965                     0.0           2.249795         4.308999            0.0              86.332293  319.859239         5.189976     110.352609               0.0          0.004439 -186.023154       1.669430              0.0          45.969291   811.210637           0.0          28.574793       4.568145          0.0   0.000000          0.000000  63.494067    70.822326       5.726496   2.548657   343.189457          4.795545      0.607139       54.665264  1063.982466        518.133515        0.0   0.000000     1.846374   9.891882          8.045508  1885.085218           0.0         0.0  1253270.056
    2018-12-31 22:00:00+00:00      0.359391              0.0   62.863490     4.584521     22.520938     12.093655         2.340463                0.0          7.565324               16.365579         2.691139         4.382387      6.466724             1.587758     31.095659                     0.0           3.856791         7.386855            0.0              90.323509  318.673717         4.324980      91.960508               0.0          0.002596 -155.360518       2.133160              0.0          45.969291   768.839623           0.0          24.723044       4.568145          0.0   0.000000          0.000000  36.103874    83.604447       5.726496   3.286427   234.098912          8.220934      0.607139       45.554387   914.239637        497.037022        0.0   0.000000     0.959162   7.457390          6.498228  1690.536792           0.0         0.0  1253270.056
    2018-12-31 23:00:00+00:00      0.278238              0.0   53.031278     4.571941     21.178631     18.084022         3.582988                0.0          7.809367               15.975922         4.069642         2.241660      6.312754             1.638976     18.060194                     0.0           9.320579        17.851565            0.0             106.069479  331.293568         3.517650      74.794546               0.0          0.001722 -108.313754       1.228886              0.0          44.874784   769.449826           0.0          18.950535       4.710899          0.0   0.000000          0.000000  43.263268    67.262312       5.905449   3.957126   123.962073         19.867257      0.626112       37.050901   760.952774        459.058276        0.0   0.000000     0.524691   8.253120          7.728429  1538.655735           0.0         0.0  1253270.056

    [8760 rows x 55 columns]
"""

import os
import sys
import datetime as dt
import urllib
import warnings

import pytz
import pandas as pd

from fips.states import States
from fips.counties import County

def _float(s,default=0.0):
    try:
        return float(s)
    except ValueError:
        return default

class RESstock(pd.DataFrame):
    """Construct a RESstock data frame

    The data frame includes the columns specified by `COLUMNS` constant, which
    maps the RESstock data to the data frame columns. The values are given in
    average Watts per housing unit. The number of units from RESstock is
    given by the `units` column. Note that the number of units is that used
    in the RESstock model, which may not be accurately reflect the actual
    number of units in any given year.
    """
    # pylint: disable=invalid-name,too-many-locals
    CACHEDIR = None
    """Cache folder path (`None` is package source folder)"""

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
    """Mapping of res RESstock columns to `RESstock` data frame columns"""

    BUILDING_TYPES = {
        "RSD": "single-family_detached",
        "RSA": "single-family_attached",
        "RSM": "multi-family_with_2_-_4_units",
        "RMM": "multi-family_with_5plus_units",
        "RMH": "mobile_home",
    }
    """Mapping of `RESstock` building types from RESstock building types"""
    
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
                "end-use-load-profiles-for-us-building-stock/2021/"\
                "resstock_amy2018_release_1/timeseries_aggregates"
            btype = self.BUILDING_TYPES[building_type]
            if county is None:
                url = f"{root}/by_state/state={state.upper()}/{state.lower()}-{btype}.csv"
            else:
                fips = County(ST=state,COUNTY=county).FIPS
                url = f"{root}/by_county/state={state.upper()}/g{fips[:2]}0{fips[2:]}0-{btype}.csv"
            try:
                data = pd.read_csv(url)
            except urllib.error.HTTPError as err:

                # download error (most likely no data in RESstock)
                warnings.warn(f"RESstock building type '{btype}' has no data ({err})")

                # create all zeros dataframe
                ndx = pd.date_range(
                    start="2018-01-01 05:00:00+00:00",
                    end="2019-01-01 04:00:00+00:00",
                    freq=freq)
                zeros = [0.0]*len(ndx)
                data = pd.DataFrame(data={x:zeros for x in self.COLUMNS},index=ndx)
                data.index.name = "timestamp"
                data.reset_index(inplace=True)
                data["units_represented"] = 0.0

            data.to_csv(cache,compression="gzip" if cache.endswith(".gz") else None)

        # load data from cache
        data = pd.read_csv(cache,dtype=str,na_filter=False,low_memory=False)
        data.set_index(["timestamp"],inplace=True)
        data.index = (pd.DatetimeIndex(data.index,tz=pytz.timezone("EST")) \
            - dt.timedelta(minutes=15)).tz_convert(pytz.UTC)

        # capture number of housing units
        units = data["units_represented"].astype(float)
        if units.min() != units.max():
            warnings.warn(f"{state=} {county=} number of units changes (using max)")
        units = units.max()

        # restructure data
        data.drop([x for x in data.columns if x not in self.COLUMNS],inplace=True,axis=1)
        data.rename(self.COLUMNS,inplace=True,axis=1)
        for value in self.COLUMNS.values():
            data[value] = [_float(x)/units*1000 for x in data[value]]

        data["units"] = units

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
