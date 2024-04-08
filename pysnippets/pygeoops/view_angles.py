from matplotlib import pyplot as plt
import pygeoops
import shapely
import shapely.plotting as plotter

viewpoint = shapely.Point(0, 0)
visible_geom = shapely.box(1, 0, 2, 1)
start_angle, end_angle = pygeoops.view_angles(viewpoint, visible_geom)
print(f"{start_angle=}, {end_angle=}")
# start_angle=0.0, end_angle=45.0

plotter.plot_points(viewpoint, color="red")
plotter.plot_polygon(visible_geom)
plt.show()
