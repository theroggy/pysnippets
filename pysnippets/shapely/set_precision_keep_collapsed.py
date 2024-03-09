import matplotlib.pyplot as plt
import shapely
import shapely.plotting as plotter

poly1 = shapely.Polygon([(0, 0), (0, 10), (10, 10), (5, 0), (0, 0)])
poly2 = shapely.Polygon([(5, 0), (8, 7), (10, 7), (10, 0), (5, 0)])
poly3 = shapely.box(15, 0, 25, 5)

intersection_nogridsize = poly1.intersection(poly2)
test = shapely.MultiPolygon([poly3, intersection_nogridsize])

plotter.plot_polygon(test)
# plotter.plot_polygon(poly3)
plt.show()

intersection_gridsize_keep = shapely.set_precision(
    test, grid_size=1, mode="keep_collapsed"
)
print(f"{intersection_gridsize_keep=}")
