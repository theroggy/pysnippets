import tempfile
from pathlib import Path

import geopandas as gpd
from osgeo import gdal, ogr

gdal.UseExceptions()

tmp_dir = Path(tempfile.gettempdir())

# Create a KML via the gdal python API
kml_gdal_path = tmp_dir / "polygon-parcel-gdal-kml.kml"

ds = ogr.GetDriverByName("KML").CreateDataSource(kml_gdal_path)
lyr = ds.CreateLayer("src_lyr", geom_type=ogr.wkbNone)

field = ogr.FieldDefn("text_1", ogr.OFTString)
lyr.CreateField(field)
field = ogr.FieldDefn("text_2", ogr.OFTString)
lyr.CreateField(field)
field = ogr.FieldDefn("text_3", ogr.OFTString)
lyr.CreateField(field)

f = ogr.Feature(lyr.GetLayerDefn())
f.SetField("text_1", "row_1")
f.SetField("text_2", "row_1")
f.SetField("text_3", "row_1")
lyr.CreateFeature(f)
ds = None

# Print the KML file content
print(f"KML file content:\n{kml_gdal_path.read_text()}")

# Read the KML via the gdal python API
kml_gdal_ds = ogr.GetDriverByName("KML").Open(str(kml_gdal_path))
kml_gdal_lyr = kml_gdal_ds.GetLayer()

# List the columns in the KML layer
print("gdal columns:", [field.name for field in kml_gdal_lyr.schema])
