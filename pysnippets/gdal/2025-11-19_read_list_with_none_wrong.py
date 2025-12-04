"""Test reading a Parquet file with list fields containing None values."""

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from osgeo import gdal
from osgeo import ogr

gdal.UseExceptions()
ogr.UseExceptions()

path = "C:/temp/temp.parquet"

# Create a Parquet file with list fields containing None values.
# Create the file with pyarrow.
table = pa.table(
    {
        "list_int_with_null": [[0, 1, None]],
        "list_string_with_null": [["a", "b", None]],
    }
)
pq.write_table(table, path)

"""
# Creating the Parquet file with OGR doesn't work, as the is an error when
# trying to write None as an element of the list in a list field.
driver = ogr.GetDriverByName("Parquet")
ds = driver.CreateDataSource(path)
lyr = ds.CreateLayer("lyr", geom_type=ogr.wkbNone)

lyr.CreateField(ogr.FieldDefn("int_list", ogr.OFTInteger64List))
lyr.CreateField(ogr.FieldDefn("str_list", ogr.OFTStringList))

f = ogr.Feature(lyr.GetLayerDefn())
f.SetFieldInteger64List(0, [1, 2, None])
f.SetFieldStringList(1, ["a", "b", None])
lyr.CreateFeature(f)

# Save and close the data source
ds = None
"""

# Reopen the data source and read back the feature
ds = ogr.Open(path)
lyr = ds.GetLayer(0)
f = lyr.GetNextFeature()
print(f.GetFieldAsInteger64List(0))
print(f.GetFieldAsStringList(1))
ds = None

# Clean up
gdal.Unlink(path)
