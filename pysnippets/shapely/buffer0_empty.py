import shapely
from shapely import LineString

print(shapely.make_valid(LineString([(-77.4664, 38.41264), (-77.4664, 38.41266)])))
# LINESTRING (-77.4664 38.41264, -77.4664 38.41266)
