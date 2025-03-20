import matplotlib.pyplot as plt
import shapely
import shapely.plotting as plotter

centers = [
   [(366.99763488064747, -45.610000000000014)],
   [(366.2381975042589, -45.339682883479995)],
   [(366.0603171165201, -45.161802495741185)],
   [(365.7900000000001, -44.40236511935221)]
]

polygons = shapely.voronoi_polygons(shapely.MultiPoint(centers))
print(len(polygons.geoms))
fig, axes = plt.subplots(ncols=len(polygons.geoms) + 1, sharex=True, sharey=True)
for idx, polygon in enumerate(polygons.geoms):
    plotter.plot_polygon(polygon, axes[idx])
for ax in axes:
    ax.set_aspect('equal', adjustable='box')
    for center in centers:
        plotter.plot_points(shapely.Point(center[0]), color="red", ax=ax)

for polygon in polygons.geoms:
    plotter.plot_polygon(polygon, axes[-1])

plt.show()
