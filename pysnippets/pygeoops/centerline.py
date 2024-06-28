import geopandas as gpd
import pygeoops
import shapely

wkt = "POLYGON ((0 0, 0 8, -2 10, 4 10, 2 8, 2 2, 10 2, 10 0, 0 0))"
poly = shapely.from_wkt(wkt)

gdf = gpd.GeoDataFrame([{"name": "L-shape", "geometry": poly}], crs="epsg:31370")
gdf.geometry = pygeoops.centerline(gdf.geometry)
print(gdf)
#       name                                           geometry
# 0  L-shape  MULTILINESTRING ((1.000 8.750, 1.137 1.116, 8....
