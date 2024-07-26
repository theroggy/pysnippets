"""
https://gis.stackexchange.com/questions/177583/interpolating-every-x-distance-along-line-in-shapely/484268#484268
"""

from matplotlib import pyplot as plt
import shapely
import shapely.plotting as plotter

line = shapely.LineString([(0, 0), (10, 0), (10, 4)])
line2 = line.segmentize(4)
points = shapely.points(line2.coords)

plotter.plot_line(line)
plotter.plot_points(points, color="red")
plt.show()
