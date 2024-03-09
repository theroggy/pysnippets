import matplotlib.pyplot as plt
import shapely
import shapely.plotting as plotter

poly1 = shapely.box(0, -0.4, 5, 5)
poly2 = shapely.box(5, -0.4, 15, 0.4)
poly3 = shapely.box(15, -0.4, 25, 5)

test = shapely.union_all([poly1, poly2, poly3])
plotter.plot_polygon(test)
plt.show()

test_precision = shapely.set_precision(test, grid_size=1)
print(f"{test_precision=}")
plotter.plot_polygon(test_precision)
plt.show()
