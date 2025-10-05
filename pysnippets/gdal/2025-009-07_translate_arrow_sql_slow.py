import os
import tempfile
import time
from pathlib import Path
from osgeo import gdal, ogr

ogr.UseExceptions()

# Create input test file with a datetime field with a date in it
input_path = "C:/temp/lds-nz-building-outlines/nz-building-outlines.gpkg"
output_path = "C:/temp/test_output.gpkg"

where = "ST_NPOINTS(geom) > 2000"
sql = f'SELECT * FROM "nz_building_outlines" WHERE {where}'

print("=== filter using where, with arrow ===")
start = time.perf_counter()
# os.environ["OGR2OGR_USE_ARROW_API"] = "YES"
os.environ["OGR_GPKG_STREAM_BASE_IMPL"] = "NO"
options = gdal.VectorTranslateOptions(where=where)
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path, options=options)
output_ds = None
print(f"took {time.perf_counter() - start} seconds")

print("=== filter using where, without arrow ===")
start = time.perf_counter()
# os.environ["OGR2OGR_USE_ARROW_API"] = "NO"
os.environ["OGR_GPKG_STREAM_BASE_IMPL"] = "YES"
options = gdal.VectorTranslateOptions(where=where)
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path, options=options)
output_ds = None
print(f"took {time.perf_counter() - start} seconds")

print("=== filter using sql, with arrow ===")
start = time.perf_counter()
#os.environ["OGR2OGR_USE_ARROW_API"] = "YES"
os.environ["OGR_GPKG_STREAM_BASE_IMPL"] = "NO"
options = gdal.VectorTranslateOptions(SQLStatement=sql)
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path, options=options)
output_ds = None
print(f"took {time.perf_counter() - start} seconds")

print("=== filter using sql, without arrow ===")
start = time.perf_counter()
# os.environ["OGR2OGR_USE_ARROW_API"] = "NO"
os.environ["OGR_GPKG_STREAM_BASE_IMPL"] = "YES"
options = gdal.VectorTranslateOptions(SQLStatement=sql)
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path, options=options)
output_ds = None
print(f"took {time.perf_counter() - start} seconds")
