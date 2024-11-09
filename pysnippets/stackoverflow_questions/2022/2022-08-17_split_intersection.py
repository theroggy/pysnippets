"""
https://stackoverflow.com/questions/73379418/spliting-intersecting-polygons-in-the-middle
https://stackoverflow.com/staging-ground/79153690
"""
import shapely
import shapely.ops
from matplotlib import pyplot as plt
from shapely.geometry import box, LineString, Polygon, Point
from shapely import plotting as plotter

def distribute_intersections(poly1, poly2, grid_size=0.0001):
    intersection_points = poly1.boundary.intersection(poly2.boundary, grid_size=grid_size)
    intersection_line = LineString(shapely.get_coordinates(intersection_points))
    intersections = poly1.intersection(poly2, grid_size=grid_size)
    split_lines = shapely.intersection(intersections, intersection_line, grid_size=grid_size)

    # Loop through all split lines found and apply them one by one
    poly1_distributed = poly1
    poly2_distributed = poly2
    for split_line in shapely.get_parts(split_lines):
        if isinstance(split_line, Point):
            continue

        # For both polygons, split them with the current split line and remove the part
        # that is ~covered by the other polygon
        poly1_distributed = shapely.ops.split(poly1_distributed, split_line)
        poly1_distributed = _remove_covered_parts(poly1_distributed, poly2, grid_size)
        poly2_distributed = shapely.ops.split(poly2_distributed, split_line)
        poly2_distributed = _remove_covered_parts(poly2_distributed, poly1, grid_size)

    return poly1_distributed, poly2_distributed

def _remove_covered_parts(poly_split, intersecting_poly, grid_size):
    for poly in shapely.get_parts(poly_split):
        intersection = poly.intersection(intersecting_poly, grid_size=grid_size)
        if intersection.area > 0.9 * poly.area:
            continue

        return poly

poly1 = box(0, 0, 10, 10)
poly2 = box(7, 7, 15, 20)
poly1_result, poly2_result = distribute_intersections(poly1, poly2)

circle1 = Point(0, 5).buffer(6, resolution=4)
circle2 = Point(0, 12).buffer(6, resolution=4)
circle1_result, circle2_result = distribute_intersections(circle1, circle2)

circle3 = Point(5, 0).buffer(6, resolution=4)
star1 = Polygon([
    (8, 0), (12, -1), (13, -5), (14, -1), (20, 0), (16, 1), (18, 6), (14, 4),
    (8, 3), (12, 2), (8, 0)
])
circle3_result, star1_result = distribute_intersections(circle3, star1)

# Plot results
_, ax = plt.subplots(ncols=3)
plotter.plot_polygon(poly1_result, ax=ax[0], color="red", alpha=0.1)
plotter.plot_polygon(poly2_result, ax=ax[0], color="green", alpha=0.1)

plotter.plot_polygon(circle1_result, ax=ax[1], color="red", alpha=0.1)
plotter.plot_polygon(circle2_result, ax=ax[1], color="green", alpha=0.1)

plotter.plot_polygon(circle3_result, ax=ax[2], color="red", alpha=0.1)
plotter.plot_polygon(star1_result, ax=ax[2], color="green", alpha=0.1)

for cur_ax in ax:
    cur_ax.set_aspect("equal")
plt.show()
