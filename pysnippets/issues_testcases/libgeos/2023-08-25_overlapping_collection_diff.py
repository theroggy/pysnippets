"""
Reported in https://github.com/libgeos/geos/issues/948
"""

import shapely

# Difference of geom: 1 polygon, geom: GeometryCollection of 2 overlapping polygons
# Result: TopologyException
geom = shapely.Polygon([(0, 0), (50, 0), (50, 50), (0, 50), (0, 0)])
geom_collection = shapely.GeometryCollection(
    [
        shapely.Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]),
        shapely.Polygon([(5, 0), (20, 0), (20, 10), (5, 10), (5, 0)]),
    ]
)
print(f"versions: shapely: {shapely.__version__}, geos-C-api: {shapely.geos_capi_version_string}")

print(f"is simple poly valid? {shapely.is_valid_reason(geom)}")
print(f"is collection valid? {shapely.is_valid_reason(geom_collection)}")

try:
    result = shapely.difference(geom, geom_collection)
except Exception as ex:
    print(f"Exception raised: {ex}")
