"""Script to check how repeated points are treated by several functions.

- set_precision: repeated points are removed.
- is_valid: repeated points are not considered as making a polygon invalid.
- make_valid: repeated points are NOT removed.
"""

import shapely
from shapely import count_coordinates


# Behaviour of set_precision and remove_repeated_points towards (nearly) repeated points
print("Test set_precision with a polygon with (nearly)repeated points")
poly = shapely.Polygon([(0, 0), (0.9, 0), (1, 0), (1, 1), (0, 1), (0, 0.9), (0, 0)])
poly_no_dups = shapely.remove_repeated_points(poly)
rounded = shapely.set_precision(poly, grid_size=1)
rounded_no_dups = shapely.remove_repeated_points(rounded)

print(f"{count_coordinates(poly)=}")
print(f"{count_coordinates(poly_no_dups)=}")
print(f"{count_coordinates(rounded)=}")
print(f"{count_coordinates(rounded_no_dups)=}")

poly = shapely.Polygon([(0, 0), (1, 0), (1, 0), (1, 1), (0, 1), (0, 0.9), (0, 0)])
poly_no_dups = shapely.remove_repeated_points(poly)
rounded = shapely.set_precision(poly, grid_size=1)
rounded_no_dups = shapely.remove_repeated_points(rounded)

print(f"{count_coordinates(poly)=}")
print(f"{count_coordinates(poly_no_dups)=}")
print(f"{count_coordinates(rounded)=}")
print(f"{count_coordinates(rounded_no_dups)=}")

# Behaviour of make_valid
print("Test make_valid with a polygon with repeated points")
poly_wkt = "POLYGON ((0 0, 1 0, 1 0, 1 1, 0 1, 0 0.9, 0 0))"
poly = shapely.from_wkt(poly_wkt)
assert poly.is_valid
poly_valid = shapely.make_valid(poly)
print(f"{count_coordinates(poly)=}")
print(f"{count_coordinates(poly_valid)=}")
