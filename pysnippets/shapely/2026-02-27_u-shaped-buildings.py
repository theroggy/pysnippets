"""Script to test with options to fill up u-shaped buildings."""

from shapely import Polygon
from shapely import plotting as plotter
import matplotlib.pyplot as plt

u_shape = Polygon([(0, 0), (0, 10), (3, 10), (3, 3), (7, 3), (7, 10), (10, 10), (10, 0)])
l_shape = Polygon([(0, 0), (0, 10), (3, 10), (3, 3), (10, 3), (10, 0)])
u_shape_breed = Polygon([(0, 0), (0, 10), (2, 10), (2, 2), (8, 3), (8, 10), (10, 10), (10, 0)])

# Try filling up the shape using a buffer
u_shape_pos_buffer = u_shape.buffer(2.5, join_style="mitre")
u_shape_filled_buffer = (
    u_shape.buffer(2.5, join_style="mitre")
    .buffer(-2.5, join_style="mitre")
)
l_shape_pos_buffer = l_shape.buffer(2.5, join_style="mitre")
l_shape_filled_buffer = (
    l_shape.buffer(2.5, join_style="mitre")
    .buffer(-2.5, join_style="mitre")
)
u_shape_breed_pos_buffer = u_shape_breed.buffer(2.5, join_style="mitre")
u_shape_breed_filled_buffer = (
    u_shape_breed.buffer(2.5, join_style="mitre")
    .buffer(-2.5, join_style="mitre")
)

# Try filling up the shape using a convex hull
u_shape_filled_convex_hull = u_shape.convex_hull
l_shape_filled_convex_hull = l_shape.convex_hull
u_shape_breed_filled_convex_hull = u_shape_breed.convex_hull

# Try filling up the shape using a rotated rectangle
u_shape_filled_rotated_rectangle = u_shape.minimum_rotated_rectangle
l_shape_filled_rotated_rectangle = l_shape.minimum_rotated_rectangle
u_shape_breed_filled_rotated_rectangle = u_shape_breed.minimum_rotated_rectangle

# Plot the results
_, ax = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=True)
# Make sure x and y axes are the same for all subplots
for i in range(len(ax)):
    for j in range(len(ax[i])):
        ax[i, j].set_aspect("equal")

ax[0, 0].set_title("U-shape, buffer")
plotter.plot_polygon(u_shape_filled_buffer, ax=ax[0, 0], color="red", alpha=0.3)
plotter.plot_polygon(u_shape_pos_buffer, ax=ax[0, 0], facecolor="none", edgecolor="grey", linestyle="--")
plotter.plot_polygon(u_shape, ax=ax[0, 0], color="green", alpha=0.3)

ax[1, 0].set_title("U-shape, convex hull")
plotter.plot_polygon(u_shape_filled_convex_hull, ax=ax[1, 0], color="red", alpha=0.3)
plotter.plot_polygon(u_shape, ax=ax[1, 0], color="green", alpha=0.3)

ax[2, 0].set_title("U-shape, rotated rectangle")
plotter.plot_polygon(u_shape_filled_rotated_rectangle, ax=ax[2, 0], color="red", alpha=0.3)
plotter.plot_polygon(u_shape, ax=ax[2, 0], color="green", alpha=0.3)

ax[0, 1].set_title("L-shape, buffer")
plotter.plot_polygon(l_shape_filled_buffer, ax=ax[0, 1], color="red", alpha=0.3)
plotter.plot_polygon(l_shape_pos_buffer, ax=ax[0, 1], facecolor="none", edgecolor="grey", linestyle="--")
plotter.plot_polygon(l_shape, ax=ax[0, 1], color="green", alpha=0.3)

ax[1, 1].set_title("L-shape, convex hull")
plotter.plot_polygon(l_shape_filled_convex_hull, ax=ax[1, 1], color="red", alpha=0.3)
plotter.plot_polygon(l_shape, ax=ax[1, 1], color="green", alpha=0.3)

ax[2, 1].set_title("L-shape, rotated rectangle")
plotter.plot_polygon(l_shape_filled_rotated_rectangle, ax=ax[2, 1], color="red", alpha=0.3)
plotter.plot_polygon(l_shape, ax=ax[2, 1], color="green", alpha=0.3)

ax[0, 2].set_title("U-shape breed, buffer")
plotter.plot_polygon(u_shape_breed_filled_buffer, ax=ax[0, 2], color="red", alpha=0.3)
plotter.plot_polygon(u_shape_breed_pos_buffer, ax=ax[0, 2], facecolor="none", edgecolor="grey", linestyle="--")
plotter.plot_polygon(u_shape_breed, ax=ax[0, 2], color="green", alpha=0.3)

ax[1, 2].set_title("U-shape breed, convex hull")
plotter.plot_polygon(u_shape_breed_filled_convex_hull, ax=ax[1, 2], color="red", alpha=0.3)
plotter.plot_polygon(u_shape_breed, ax=ax[1, 2], color="green", alpha=0.3)

ax[2, 2].set_title("U-shape breed, rotated rectangle")
plotter.plot_polygon(u_shape_breed_filled_rotated_rectangle, ax=ax[2, 2], color="red", alpha=0.3)
plotter.plot_polygon(u_shape_breed, ax=ax[2, 2], color="green", alpha=0.3)

plt.show()
