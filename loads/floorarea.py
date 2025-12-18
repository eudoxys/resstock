"""Commercial floor area data accessor

Examples:

Get the commercial building floor areas for Alameda County CA

    from loads.floorarea import Floorarea
    print(Floorarea("CA","Alameda"))

References: 

- https://data.openei.org/submissions/906
"""

import os
import urllib

import pandas as pd

from fips.counties import County

class Floorarea(pd.DataFrame):
    """Commercial building floor area data frame implementation"""
    CACHEDIR = None
    YEAR = 2019
    REGIONS = {
    }
    BUILDING_TYPES = {
        "apartment": ["CLL"],
        "full_service_restaurant": ["CLF"],
        "hotel": ["CSL"],
        "no_match": [],
        "office": ["CSO","CMO","CLO"],
        "outpatient": ["CSH"],
        "quick_service_restaurant": ["CSF"],
        "retail": ["CMS"],
        "school": ["CME","CSE"],
        "strip_mall": ["CSR"],
        "supermarket": ["CMR"],
        "warehouse": ["CMW"],
        "hospital": ["CLH"],
    }

    def __init__(self,
        state:str=None,
        county:str=None,
        year:int=None,
        ):
        """Commercial floor area data frame constructor

        Arguments:

        - `state`: specify the state abbreviation (required)

        - `county`: specify the county name (required)

        - `year`: specify the year on which the floor area is based
          (default most recent in `Units()`)
        """
        if self.CACHEDIR is None:
            self.CACHEDIR = os.path.join(os.path.dirname(__file__),".cache")
        os.makedirs(self.CACHEDIR,exist_ok=True)

        if year is None:
            year = self.YEAR

        # load cunty commercial floor area data
        cache = os.path.join(self.CACHEDIR,"floorarea.csv.gz")
        if not os.path.exists(cache):
            root = "https://data.openei.org/files/906/{year}%20Commercial%20Building%20Inventory%20-%20{region}.xlsb"
            data = []
            for n,region in enumerate([
                "South Central",
                "Northeast",
                "South Atlantic",
                "Midwest",
                "West",
                ]):

                file = os.path.join(self.CACHEDIR,f"region{n}_floorarea.csv.gz")
                if not os.path.exists(file):
                    # print("Downloading",region,"...",flush=True)
                    result = pd.read_excel(root.format(
                            region=region.replace(" ","%20"),
                            year=year
                            ),
                        sheet_name="County",
                        usecols=["statecode","countyid","doe_prototype","area_sum"]
                        ).dropna()
                    result = result.groupby(["statecode","countyid","doe_prototype"]).sum().reset_index()
                    result.columns = ["ST","FIPS","BUILDING_TYPE","FLOORAREA"]
                    result.to_csv(file,index=False,header=True,compression="gzip")
                else:
                    result = pd.read_csv(file)
                result.FLOORAREA = result.FLOORAREA.astype(float)
                data.append(result)
            data = pd.concat(data)
            data.to_csv(cache,index=False,header=True,compression="gzip")
        else:
            data = pd.read_csv(cache)
        data.FIPS=[f"{x:05d}" for x in data.FIPS]
        data.BUILDING_TYPE = ["|".join(self.BUILDING_TYPES[x]) for x in data.BUILDING_TYPE]

        if not state and not county:
            super().__init__(data)
        elif state and not county:
            super().__init__(data.set_index("ST").loc[state])
        else:
            fips = County(ST=state,COUNTY=county).FIPS
            super().__init__(data.set_index(["ST","FIPS"]).sort_index().loc[state,fips])

if __name__ == "__main__":

    print(Floorarea())
    print(Floorarea("CA"))
    print(Floorarea("CA","Alameda"))
