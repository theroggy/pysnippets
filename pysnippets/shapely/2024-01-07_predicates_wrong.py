from matplotlib import pyplot as plt
import shapely
import shapely.plotting as plotter

line = shapely.LineString([(0.0,0.0), (-2.0,-3.0)])
point = shapely.Point(-0.2, -0.3)

print(line.intersects(point))

plotter.plot_line(line)
plotter.plot_points(point, color="red")

plt.show()
