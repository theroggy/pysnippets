from osgeo import gdal
import geopandas as gpd
from shapely import box

gdal.UseExceptions()

# Input
path = "tmp/tmp.gpkg"
gdf = gpd.GeoDataFrame(geometry=[box(0, 0, 10, 10)], crs=31370)
print(f"before {gdf.total_bounds.tolist()=}")
gdf.to_file(path)

# Translate
ds = gdal.OpenEx(path, nOpenFlags=gdal.OF_UPDATE)
result = ds.ExecuteSQL("UPDATE tmp SET geom = ST_Translate(geom, 10, 10, 0)")
ds.ReleaseResultSet(result)
ds = None

# Result
gdf = gpd.read_file(path)
print(f"after {gdf.total_bounds.tolist()=}")
