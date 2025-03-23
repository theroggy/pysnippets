import warnings

import pyogrio

file = "C:\Temp\polygon_parcel\polygon-parcel.gpkg"

with open(file, "rb") as f:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", ".*has GPKG application_id.*", RuntimeWarning)
        pyogrio.read_dataframe(f)
