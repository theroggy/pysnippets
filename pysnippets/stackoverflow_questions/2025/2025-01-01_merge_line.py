import geopandas as gp
import shapely
from shapely.geometry import LineString, Polygon

# Draw a polygon that is 100 x 100 units, starting at coordinates 0, 0
polygon = Polygon([(50, 0), (50, 100), (100, 100), (100, 0)])

# Convert the polygon to a geodataframe
polygon = gp.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[polygon])

# Draw a horizontal line that starts at coordinates 50, 0 and is 200 units long
line = LineString([(0, 50), (75, 50), (70, 35), (55, 40), (250, 50)])

# Convert the line to a geodataframe
line = gp.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[line])

# print(line)

# Intersect the line with the polygon
intersection = line.intersection(polygon)

print(f"{intersection=}")

# Recreate the intersection line from its coordinates
intersection_line = shapely.linestrings(shapely.get_coordinates(intersection))

print(f"{intersection_line=}")
