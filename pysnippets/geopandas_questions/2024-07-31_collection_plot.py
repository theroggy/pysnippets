import numpy as np
import shapely
from shapely.geometry import Point, Polygon
from shapely.plotting import plot_polygon

poly_with_hole = Polygon(
    np.array([[0, 0], [0, 10], [10, 10], [10, 0]]),
    holes=[np.array([[7, 0], [5, 2], [3, 0]])],
)

# Intersection with the original, invalid polygon gives a GeometryCollection
bug_poly = poly_with_hole.intersection(Point(5, 5).buffer(6))

print(f"{bug_poly=}")
for geom in bug_poly.geoms:
    print(f"bug_poly.{geom=}")
# bug_poly=<GEOMETRYCOLLECTION (POLYGON ((0 8.315, 0.011 8.333, 0.362 8.806, 0.757 9.24...>
# bug_poly.geom=<POLYGON ((0 8.315, 0.011 8.333, 0.362 8.806, 0.757 9.243, 1.194 9.638, 1.66...>       
# bug_poly.geom=<LINESTRING (7 0, 3 0)>

# Error
# plot_polygon(bug_poly)

# But... the input polygon is invalid!
print(f"{poly_with_hole.is_valid=}")
# poly_with_hole.is_valid=False

poly_with_hole_valid = shapely.make_valid(poly_with_hole)
print(f"{poly_with_hole_valid.is_valid=}")
# poly_with_hole_valid.is_valid=True

print(f"{poly_with_hole_valid=}")
for geom in poly_with_hole_valid.geoms:
    print(f"poly_with_hole_valid.{geom=}")
# poly_with_hole_valid=<GEOMETRYCOLLECTION (POLYGON ((0 0, 0 10, 10 10, 10 0, 7 0, 3 0, 0 0)), LINE...>
# poly_with_hole_valid.geom=<POLYGON ((0 0, 0 10, 10 10, 10 0, 7 0, 3 0, 0 0))>
# poly_with_hole_valid.geom=<LINESTRING (7 0, 5 2, 3 0)>

poly_with_hole_valid_poly = poly_with_hole_valid.geoms[0]

# Intersection with the valid polygon with only polygons can be plotted
poly = poly_with_hole_valid_poly.intersection(Point(5, 5).buffer(6))
plot_polygon(bug_poly)


# Generic solution to extract only polygons from a collection
import pygeoops

poly_with_hole_valid_extracted = pygeoops.collection_extract(poly_with_hole_valid, 3)
print(f"{poly_with_hole_valid_extracted=}")
# poly_with_hole_valid_extracted=<POLYGON ((0 0, 0 10, 10 10, 10 0, 7 0, 3 0, 0 0))>
