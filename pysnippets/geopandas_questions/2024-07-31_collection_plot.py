import numpy as np
from shapely.geometry import Point, Polygon
from shapely.plotting import plot_polygon

poly_with_hole = Polygon(
    np.array([[0, 0], [0, 10], [10, 10], [10, 0]]),
    holes=[np.array([[7, 0], [5, 2], [3, 0]])],
)
bug_poly = poly_with_hole.intersection(Point(5, 5).buffer(6))

print(f"bug_poly.{bug_poly=}")
for geom in bug_poly.geoms:
    print(f"bug_poly.{geom=}")
# bug_poly.bug_poly=<GEOMETRYCOLLECTION (POLYGON ((0 8.315, 0.011 8.333, 0.362 8.806, 0.757 9.24...>
# bug_poly.geom=<POLYGON ((0 8.315, 0.011 8.333, 0.362 8.806, 0.757 9.243, 1.194 9.638, 1.66...>
# bug_poly.geom=<LINESTRING (7 0, 3 0)>

plot_polygon(bug_poly.geoms[0])
