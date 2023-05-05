import os
os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd
import shapely
from shapely.geometry import Point

points = {"geometry": [Point(0, 0, 2), Point(0, 1, 2), Point(1, 0, 2)]}
gdf = gpd.GeoDataFrame(points)
c = shapely.get_coordinates(gdf.geometry, include_z=True)

print(c)
"""
[[0. 0. 2.]
[0. 1. 2.]
[1. 0. 2.]]
"""
