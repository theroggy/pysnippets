import shapely
import shapely.ops

pts = shapely.from_wkt("MULTIPOINT (-8e-16 0, -9e-16 0)")
line = shapely.from_wkt("LINESTRING (-1.5 0, 1.5 0)")
print(shapely.ops.split(line, pts))
