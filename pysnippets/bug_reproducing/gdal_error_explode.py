import os
from osgeo import gdal

# There is some weird behaviour here:
#   - If only gdal.UseExceptions() is used, an exception is thrown, but not an
#     interesting one:
#   - If gdal.UseExceptions() + os.environ["CPL_DEBUG"] = "ON", the debug logging stops
#     being written too soon and no exception is thrown.
#   - If only os.environ["CPL_DEBUG"] = "ON", the debug logging contains all necessary
#     information, but obviously no exception is thrown.

# gdal.UseExceptions()
os.environ["CPL_DEBUG"] = "ON"

src = "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"
dst = "/vsimem/output.gpkg"
dst = "C:/Temp/output.gpkg"
options = gdal.VectorTranslateOptions(explodeCollections=True)
ds_output = gdal.VectorTranslate(srcDS=src, destNameOrDestDS=dst, options=options)
