from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import shapely
from shapely.plotting import plot_line, plot_polygon

poly1 = shapely.box(2, 0, 4, 3)
poly2 = shapely.box(0, 1, 2, 2)

lines = []
# Intersecting lines
intersecting_lines = poly1.boundary.intersection(poly2.boundary)
lines.extend(shapely.get_parts(shapely.line_merge(intersecting_lines)))

# Non intersecting boundaries
lines.extend(
    shapely.get_parts(shapely.line_merge(poly1.boundary.difference(intersecting_lines)))
)
lines.extend(
    shapely.get_parts(shapely.line_merge(poly2.boundary.difference(intersecting_lines)))
)

# Plot
fig, ax = plt.subplots(ncols=2, figsize=(15, 15))
plot_polygon(poly1, ax=ax[0], color="red")
plot_polygon(poly2, ax=ax[0])

colors = []
for line, color in zip(lines, mcolors.TABLEAU_COLORS):
    plot_line(line, ax=ax[1], color=color)

plt.show()
