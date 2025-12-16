"""RESstock data accessor

Generates electric load model for residential, commercial, industrial,
agricultural, and public sectors. Two types of data frame are generated
depending on whether `building_type` is specified.

If `building_type` is specified, then the raw end-use data for that building
type is returned, the columns of which depend on the building type.  If
`building_type` is not specified, then the compiled end-use data for the
entire sector is returned, with the contribution from each building type in
columns of MW and per-unit total for electric and non-electric base, cooling,
heating, and total loads.

Examples:

To print the raw residential single-family detached house loads in Alameda
County CA as a table.

    loads CA Alameda residential --building_type=RSFD

To get the compiled residential loads in Alameda County CA in CSV format

    loads CA Alameda residential --format=csv

Caveats:

* Compiling data can be time consuming. To help with performance data is cached
  locally in the package library. However, 
"""

import sys
import argparse
import warnings

import pandas as pd

# pylint: disable=unused-import
from loads.resstock import RESstock
from loads.residential import Residential

E_OK = 0
E_FAILED = 1
E_SYNTAX = 2

def main(*args:list[str]) -> int:
    """RESstock form accessor main command line processor

    Argument:

        - `*args`: command line arguments (`None` is `sys.argv`)

    Returns:

        - `int`: return/exit code
    """
    # pylint: disable=too-many-return-statements,too-many-branches
    try:

        # support direct call to main
        if args:
            sys.argv = [__file__] + list(args)

        # setup command line parser
        parser = argparse.ArgumentParser(
            prog="resstock",
            description="RESstock form data accessor",
            epilog="See https://www.eudoxys.com/resstock for documentation. ",
            )
        parser.add_argument("state")
        parser.add_argument("county")
        parser.add_argument("sector",
            choices=["residential","commercial","industrial","agricultural","public"]
            )
        parser.add_argument("-y","--year",
            type=int,
            help="set load model year")
        parser.add_argument("-o","--output",
            help="set output file name")
        parser.add_argument("--building_type",
            help="access raw building type stock data")
        parser.add_argument("--format",
            choices=["csv","gzip","zip","xlsx"],
            help="specify output format")
        parser.add_argument("--precision",
            type=int,
            default=3,
            help="specify output precision"
            )
        parser.add_argument("--warning",
            action="store_true",
            help="enable warning messages from python")
        parser.add_argument("--debug",
            action="store_true",
            help="enable debug traceback on exceptions")

        # parse arguments
        args = parser.parse_args()

        # setup warning handling
        if not args.warning:
            warnings.showwarning = lambda *x:print(
                f"WARNING [{__package__}]:",
                x[0],
                flush=True,
                file=sys.stderr,
                )

        # get data
        match args.sector:
            case "residential":
                source = (RESstock if args.building_type else Residential)
                kwargs = source.makeargs(**vars(args))
                data = source(**kwargs).round(args.precision)
            case "_":
                raise ValueError(f"{args.sector=} is invalid")

        # handle default output
        if args.output is None:
            if args.format is None:
                pd.options.display.max_rows = None
                pd.options.display.width = None
                pd.options.display.max_columns = None
                print(data)
            elif args.format == "csv":
                print(data.to_csv())
            else:
                raise ValueError(f"{args.format} if not valid for this output stream")
            return E_OK

        # handle CSV output
        if args.output.endswith(".csv") or args.format == "csv":
            data.to_csv(args.output)
            return E_OK

        # handle GZIP output
        if args.output.endswith(".csv.gz") or args.format == "gzip":
            data.to_csv(args.output,compression="gzip")
            return E_OK

        # handle ZIP output
        if args.output.endswith(".csv.zip") or args.format == "zip":
            data.to_csv(args.output,compression="zip")
            return E_OK

        # handle XLSX output
        if args.output.endswith(".xlsx") or args.format == "xlsx":
            data.to_excel(args.output,
                sheet_name="Form861",
                merge_cells=False)
            return E_OK

        raise ValueError(f"output format '{args.format}' for '{args.output}' is invalid")

    # pylint: disable=broad-exception-caught
    except Exception as err:

        if getattr(args,"debug"):
            raise

        print(f"ERROR [loads]: {err}")
        return E_FAILED

if __name__ == '__main__':
    pd.options.display.width = None
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    print(main("CA","Alameda","residential","--building_type=RSFD"))
    print(main("CA","Alameda","residential","--format=csv"))
