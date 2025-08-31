import sqlite3
from pathlib import Path

import pandas as pd
import pyogrio
from osgeo import gdal

gdal.UseExceptions()

# Create a sqlite file

create_new_file = False

if create_new_file:
    script_path = Path(__file__)
    path = script_path.with_suffix(".sqlite")

    df = pd.DataFrame({"name": ["foö", "bÏr"], "value": [1, 2]})

    if path.exists():
        path.unlink()
    con = sqlite3.connect(str(path))
    df.to_sql(name="test", index=True, con=con)
    con.close()
else:
    path = Path(r"C:\Users\Gebruiker\Documents\GitHub\pyogrio\bla.db")

# Open the datasource and print TestCapability of OLCStringsAsUTF8
datasource = gdal.OpenEx(str(path))
datasource_layer = datasource.GetLayer()

print(f"{datasource_layer.GetName()=}")
print(f"{datasource_layer.TestCapability(gdal.ogr.OLCStringsAsUTF8)=}")
datasource_layer = None
datasource = None

# Read and print the table
print(pyogrio.read_dataframe(str(path)))

# Determine encoding
con = sqlite3.connect(str(path))
cursor = con.cursor()
cursor.execute("PRAGMA encoding;")
encoding = cursor.fetchone()[0]
print(f"Database encoding: {encoding}")
con.close()
