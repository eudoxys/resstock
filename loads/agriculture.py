"""Agricultural load data"""

import pandas as pd

class Agriculture(pd.DataFrame):

    def __init__(self,
        state:str=None,
        county:str=None,
        ):

        data = pd.read_csv("https://data.nrel.gov/system/files/97/agriculture_EndUse.gz")

        if state is None and county is None:
            super().__init__(data)
        # elif county is None:
        #     super().__init__(data.set_index([""])


if __name__ == '__main__':
    print(Agriculture())