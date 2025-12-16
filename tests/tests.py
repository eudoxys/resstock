"""RESstock tests"""

import sys
import pandas as pd
from resstock import Residential, RESstock

state = "CA"
county = "Alameda"

print("Testing",county,state,"...",flush=True)
data = Residential(state=state,county=county)

pd.options.display.width = None
pd.options.display.max_columns = None

errors = 0
for building in sorted(RESstock.BUILDING_TYPES):
    for source in ["elec","nonelec"]:
        prefix = f"{building}_{source}"

        # check that MW enduses add up to MW totals for each building type
        enduse = data[[f"{prefix}_{x}_MW" for x in ["baseload","cooling","heating"]]]
        total = enduse.sum(axis=1)
        diff = (total - data[f"{prefix}_total_MW"]).round(6)
        if (diff != 0).any():
            print(prefix,"total MW sum test failed!",file=sys.stderr)
            errors += 1

        # check that pu totals are all unity
        if (data[f"{prefix}_total_pu"].round(6) != 1.0).any():
            print(pd.concat([enduse,data[f"{prefix}_total_pu"]],axis=1))
            errors += 1

        # check that pu enduses add up to unity
        enduse = data[[f"{prefix}_{x}_pu" for x in ["baseload","cooling","heating"]]]
        total = enduse.sum(axis=1).round(6)
        if (total != 1.0).any():
            print(prefix,"total pu sum test failed!",file=sys.stderr)
            errors += 1

if errors:
    print(f"Saving data for diagnostics to '{state}_{county}.csv'",file=sys.stderr)
    data.to_csv(f"{state}_{county}.csv",index=True,header=True)
    print(f"{errors} found!")
    exit(1)
else:
    print("No errors")

