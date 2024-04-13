"""
https://stackoverflow.com/questions/78063060/calculate-distance-to-the-closest-water-body
"""

import geopandas as gpd
from shapely import box, Point

waterbodies = gpd.GeoDataFrame(
    data={
        "name": ["river1", "lake1"],
        "geometry": [box(0, 0, 10, 1), box(5, 5, 10, 10)],
    }
)

poi = Point(0, 7)

# Get the nearest water body. If there are multiple ones at the same distance, the first
# returned one is taken.
nearest_water = waterbodies.iloc[[waterbodies.sindex.nearest(poi)[1][0]]].copy()

# Calculate the actual distance of this nearest water body
nearest_water["distance"] = nearest_water.distance(poi)

print(nearest_water)
#    name                                           geometry  distance
# 1  lake1  POLYGON ((10.00000 5.00000, 10.00000 10.00000,...       5.0
