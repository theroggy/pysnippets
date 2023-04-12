import shapely
import shapely.plotting
import matplotlib.pyplot as plt

poly1 = shapely.Polygon([(0, 0), (0, 10), (10, 10), (5, 0), (0, 0)])
poly2 = shapely.Polygon([(5, 0), (8, 7), (10, 7), (10, 0), (5, 0)])

intersection_nogridsize = poly1.intersection(poly2)
intersection_gridsize = poly1.intersection(poly2, grid_size=1)

shapely.plotting.plot_polygon(poly1, color="green")
shapely.plotting.plot_polygon(poly2, color="blue")
shapely.plotting.plot_polygon(intersection_nogridsize, color="red")
plt.show()

shapely.plotting.plot_polygon(poly1, color="green")
shapely.plotting.plot_polygon(poly2, color="blue")
shapely.plotting.plot_line(intersection_gridsize, color="red")
plt.show()
