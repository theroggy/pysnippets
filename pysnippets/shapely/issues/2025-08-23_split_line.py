import shapely

line = shapely.LineString([(1,1),(3,3)])
line2 = shapely.LineString([(1.5,1.5),(2,2)])

union = shapely.union_all([line, line2])
print(union)

for geom in union.geoms:
    print(geom)
