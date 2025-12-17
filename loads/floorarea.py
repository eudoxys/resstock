"""Commercial floor area"""

import os
import urllib

import pandas as pd

class Floorarea(pd.DataFrame):

    CACHEDIR = None
    YEAR = 2019
    REGIONS = {
    }
    BUILDING_TYPES = {

        # "CLF": "fullservicerestaurant",
        # "CLH": "hospital",
        # "CLL": "largehotel",
        # "CLO": "largeoffice",
        # "CSH": "outpatient",
        # "CMO": "mediumoffice",
        # "CSE": "primaryschool",
        # "CSF": "quickservicerestaurant",
        # "CSR": "retailstandalone",
        # "CMR": "retailstripmall",
        # "CME": "secondaryschool",
        # "CSL": "smallhotel",
        # "CSO": "smalloffice",
        # "CMW": "warehouse",

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
        state:str,
        county:str,
        ):
        """Commercial floor area data frame constructor

        Arguments:

        """
        if self.CACHEDIR is None:
            self.CACHEDIR = os.path.join(os.path.dirname(__file__),".cache")
        os.makedirs(self.CACHEDIR,exist_ok=True)

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
                    print("Downloading",region,"...",flush=True)
                    result = pd.read_excel(root.format(region=region.replace(" ","%20")),
                        sheet_name="County",
                        usecols=["statecode","countyid","doe_prototype","area_sum"]
                        ).dropna()
                    result = result.groupby(["statecode","countyid","doe_prototype"]).sum().reset_index()
                    result.columns = ["ST","FIPS","BUILDING_TYPE","FLOORAREA"]
                    result.to_csv(file,index=False,header=True,compression="gzip")
                else:
                    result = pd.read_csv(file)
                data.append(result)
            data = pd.concat(data)
            data.to_csv(cache,index=False,header=True,compression="gzip")
        else:
            data = pd.read_csv(cache)
        data.FIPS=[f"{x:05d}" for x in data.FIPS]
        data.BUILDING_TYPE = ["|".join(self.BUILDING_TYPES[x]) for x in data.BUILDING_TYPE]

        super().__init__(data)

if __name__ == "__main__":

    print(Floorarea("CA","Alameda"))