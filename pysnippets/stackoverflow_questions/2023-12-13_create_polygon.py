from matplotlib import pyplot as plt
from shapely.geometry import Polygon, MultiLineString
from shapely import get_coordinates, line_merge, make_valid
import shapely.plotting as plot

# polygon can be created
t = [[(1, 1), (1, 6)], [(1, 6), (6, 6)], [(6, 6), (6, 1)], [(1, 1), (6, 1)]]
tt = line_merge(MultiLineString(t))
p1 = Polygon(tt)

# polygon cannot be created
f = [[(3, 1), (1, 1)], [(1, 1), (1, 6)], [(1, 6), (6, 6)], [(6, 6), (6, 1)], [(6, 1), (3, 1)], [(3, 1), (5, 3)], [(5, 3), (2, 3)], [(3, 1), (2, 3)]]
ff = line_merge(MultiLineString(f))

# A MultiLineString is not iterable, so extract the coordinates explicitly
p2 = Polygon(get_coordinates(ff))
# The polygon is not valid because the coordinates weren't properly structured.
# Using make_valid() fixes this.
p2 = make_valid(p2)

# Plot result
plot.plot_polygon(p2)
plt.show()
