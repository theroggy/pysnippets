import sqlite3
from pathlib import Path

import pandas as pd
import pyogrio
from osgeo import gdal

gdal.UseExceptions()

# Create a sqlite file
script_path = Path(__file__)
df = pd.DataFrame({"name": ["foö", "bÏr"], "value": [1, 2]})
path = script_path.with_suffix(".sqlite")
if path.exists():
    path.unlink()
con = sqlite3.connect(str(path))
df.to_sql(name="test", index=True, con=con)
con.close()

datasource = gdal.OpenEx(str(path))
datasource_layer = datasource.GetLayer()

print(f"{datasource_layer.GetName()=}")
print(f"{datasource_layer.TestCapability(gdal.ogr.OLCStringsAsUTF8)=}")
datasource_layer = None
datasource = None

pyogrio.read_dataframe(str(path))
