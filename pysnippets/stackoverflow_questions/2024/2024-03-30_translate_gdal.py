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
layer = ds.GetLayer()
for feature in layer:
    geom = feature.GetGeometryRef()
    feature.SetGeometry(convexhull)
ds = None

# Result
gdf = gpd.read_file(path)
print(f"after {gdf.total_bounds.tolist()=}")
