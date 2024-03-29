from shapely import LineString, MultiLineString, polygonize, polygonize_full

lines = [
    LineString([(0, 0), (1, 1)]),
    LineString([(0, 0), (0, 1)]),
    LineString([(0, 1), (1, 1)]),
    LineString([(1, 1), (1, 0)]),
    LineString([(1, 0), (0, 0)]),
]
print(polygonize_full(lines))
print(polygonize(lines))

multiline = MultiLineString(lines)
print(polygonize_full(multiline.geoms))
print(polygonize(multiline.geoms))
