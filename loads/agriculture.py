"""Agricultural load data

Example:

    from loads import Agriculture
    print(Agriculture("CA","Alameda"))
"""

import pandas as pd

class Agriculture(pd.DataFrame):
    "Agricultural loads data frame implementation"
    def __init__(self,
        state:str=None,
        county:str=None,
        ):
        """Construct agricultural loads data frame

        - `state`: specify the state abbreviation (required)

        - `county`: specify the county name (required)
        """

        data = pd.read_csv("https://data.nrel.gov/system/files/97/agriculture_EndUse.gz")

        if state is None and county is None:
            super().__init__(data)
        elif county is None:
            super().__init__(data)
        else:
            super().__init__(data)
