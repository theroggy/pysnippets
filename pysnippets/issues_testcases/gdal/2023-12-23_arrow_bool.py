import geopandas as gpd
from osgeo import gdal

gdal.UseExceptions()
src = "https://github.com/geopandas/pyogrio/files/13750016/sample.gpkg.zip"
interesting_rows = [0, 1, 9]
src_gdf = gpd.read_file(src)

# Translate file without Arrow
dst = "C:/temp/sample_dst.gpkg"
with gdal.config_option("OGR2OGR_USE_ARROW_API", "NO"):
    ds_output = gdal.VectorTranslate(srcDS=src, destNameOrDestDS=dst)
    ds_output = None
dst_gdf = gpd.read_file(dst)
print(f"without arrow, equal: {src_gdf.foo.tolist() == dst_gdf.foo.tolist()}")

# Translate file with Arrow -> result for bool values is not correct
dst_arrow = "C:/temp/sample_dst_arrow.gpkg"
ds_output = gdal.VectorTranslate(srcDS=src, destNameOrDestDS=dst_arrow)
ds_output = None
dst_arrow_gdf = gpd.read_file(dst_arrow)
print(f"with arrow, values wrong: {src_gdf.foo.tolist() == dst_arrow_gdf.foo.tolist()}")
print(f"src foo values for rows {interesting_rows}: {src_gdf.foo[interesting_rows].tolist()}")
print(f"dst foo values for rows {interesting_rows}: {dst_gdf.foo[interesting_rows].tolist()}")
print(f"dst_arrow foo values for rows {interesting_rows}: {dst_arrow_gdf.foo[interesting_rows].tolist()}")
