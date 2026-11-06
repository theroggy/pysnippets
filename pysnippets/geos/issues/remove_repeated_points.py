"""Script to check how repeated points are treated by several functions.

- set_precision: repeated points are removed.
- is_valid: repeated points are not considered as making a polygon invalid.
- make_valid:
   - if the input polygon is valid, repeated points are NOT removed.
   - if the input polygon is invalid, repeated points are removed.
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

# Behaviour of make_valid on a valid polygon with repeated points
print("Test make_valid with a valid polygon with repeated points")
poly_wkt = "POLYGON ((0 0, 1 0, 1 0, 1 1, 0 1, 0 0.9, 0 0))"
poly = shapely.from_wkt(poly_wkt)
assert poly.is_valid
poly_valid = shapely.make_valid(poly)

print(f"{count_coordinates(poly)=}")
print(f"{count_coordinates(poly_valid)=}")

# Behavior of make_valid on an invalid polygon with repeated points
print("Test make_valid with an invalid polygon with repeated points")
poly_wkt = (
    "POLYGON ((0 10, 10 0, 10 0, 10 10, 0 0, 0 10), (5 5, 5 5, 5 5, 5 5))"
)
poly = shapely.from_wkt(poly_wkt)
assert not poly.is_valid
poly_valid = shapely.make_valid(poly)
assert poly_valid.is_valid
poly_valid_no_dups = shapely.remove_repeated_points(poly_valid)

print(f"{count_coordinates(poly)=}")
print(f"{count_coordinates(poly_valid)=}")
print(f"{poly_valid.wkt=}")
print(f"{count_coordinates(poly_valid_no_dups)=}")
