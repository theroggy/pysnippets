from shapely import line_merge, from_wkt, MultiLineString

wkt1 = 'LINESTRING (0 0 0 0, 1 1 1 1)'
wkt2 = 'LINESTRING (1 1 1 1, 2 2 2 2)'
a = from_wkt(wkt1)
b = from_wkt(wkt2)
ab = MultiLineString([a, b])
print(ab)
print(line_merge(ab))
