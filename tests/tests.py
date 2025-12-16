"""RESstock tests"""

import sys
import pandas as pd
from loads import Residential, RESstock

state = "CA"
county = "Alameda"

print("Testing",county,state,"...",flush=True)
data = Residential(state=state,county=county)

# check MW totals
errors = 0
error_index = []
for source in ["elec","nonelec"]:

    # check that MW enduses add up to MW totals
    enduse = data[[f"{source}_{x}_MW" for x in ["baseload","cooling","heating"]]]
    total = enduse.sum(axis=1)
    diff = (total - data[f"{source}_total_MW"]).round(6)
    if ( diff != 0 ).any():
        print(f"ERROR [loads.tests]: {source} MW total load test failed!",file=sys.stderr)
        error_index.extend(diff[diff!=0].index)
        errors += 1

# check that MW total and DG add up to net
diff = (data[f"elec_net_MW"] - data[f"elec_total_MW"] - data[f"elec_dg_MW"]).round(6)
if ( diff != 0 ).any():
    print("ERROR [loads.tests]: elec MW net load test failed!",file=sys.stderr)
    error_index.extend(diff[diff!=0].index)
    errors += 1

# save errors, if any
if errors:
    print(f"Saving errors '{state}_{county}_errors.csv'",file=sys.stderr)
    data.loc[error_index].to_csv(f"{state}_{county}_errors.csv",index=True,header=True)
    print(f"{errors} error found!")
    exit(1)
else:
    print("No errors")

