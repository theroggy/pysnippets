from shapely.geometry import MultiPolygon, Polygon, MultiLineString, LineString
from shapely.ops import split

multipolygon = MultiPolygon(
    [
        Polygon([(7, 10), (8, 11), (9, 11), (8, 10), (7, 9.5), (7, 10)]),
        Polygon([(9.5, 8.5), (10, 9), (10, 10), (11, 9), (9.5, 8.5)]),
    ]
)
multiline = MultiLineString(
    [
        LineString([(7, 10), (8, 10)]),
        LineString([(8, 10), (8, 11)]),
        LineString([(10, 9), (11, 9)]),
        LineString([(8, 9), (10, 9)]),
    ]
)

# Divide multipolygon by lines
for line in multiline.geoms:
    multipolygon = MultiPolygon(split(multipolygon, line).geoms)

print("Divided MultiPolygon:", multipolygon)
