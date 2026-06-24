import tempfile
from pathlib import Path

from osgeo import ogr

ogr.UseExceptions()

path = Path(tempfile.gettempdir()) / "test.kml"
ds = ogr.GetDriverByName("KML").CreateDataSource(str(path))
lyr = ds.CreateLayer("lyr", geom_type=ogr.wkbNone)

field = ogr.FieldDefn("col1", ogr.OFTString)
lyr.CreateField(field)
field = ogr.FieldDefn("col2", ogr.OFTString)
lyr.CreateField(field)

f = ogr.Feature(lyr.GetLayerDefn())
f.SetField("col1", "col1_row_1")
f.SetField("col2", "col2_row_1")
lyr.CreateFeature(f)

f = ogr.Feature(lyr.GetLayerDefn())
f.SetField("col1", "col1_row_2")
f.SetField("col2", "col2_row_2")
lyr.CreateFeature(f)

ds = None
ds = ogr.Open(str(path), ogr.OF_VECTOR | ogr.OF_READONLY)
lyr = ds.GetLayer()
for feat in lyr:
    col1 = feat.GetFieldAsString("col1")
    col2 = feat.GetFieldAsString("col2")
    print(f"Feature: col1={col1}, col2={col2}")
