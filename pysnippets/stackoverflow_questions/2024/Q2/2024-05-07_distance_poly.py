import shapely
import shapely.plotting as plotter
import matplotlib.pyplot as plt

poly = shapely.box(1, 0, 5, 4)
point1 = shapely.Point(0, 0)
point2 = shapely.Point(0, 2)
point3 = shapely.Point(0.9999999999999999, 0)
point4 = shapely.Point(0.99999999999999999, 0)
print(f"{poly.distance(point1)=}")
print(f"{poly.distance(point2)=}")
print(f"{poly.distance(point3)=}")
print(f"{poly.distance(point4)=}")
# poly.distance(point1)=1.0
# poly.distance(point2)=1.0
# poly.distance(point3)=1.1102230246251565e-16
# poly.distance(point4)=0.0

fig, ax = plt.subplots()
plotter.plot_polygon(poly, ax=ax)
plotter.plot_points(point1, ax=ax, color="green")
plotter.plot_points(point2, ax=ax, color="red")
plt.show()
