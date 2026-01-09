import matplotlib.pyplot as plt
import shapely
import shapely.plotting as plotter

centers = [
   (366.99763488064747, -45.610000000000014),
   (366.2381975042589, -45.339682883479995),
   (366.0603171165201, -45.161802495741185),
   (365.7900000000001, -44.40236511935221)
]

fig, axes = plt.subplots(ncols=len(centers) + 1, nrows=2)

for factor_idx, factor in enumerate([1, 10]):
    scaled_centers = [[(x * factor, y * factor)] for (x, y) in centers]
    points = shapely.MultiPoint(scaled_centers)
    print(f"Points: {points}")
    polygons = shapely.voronoi_polygons(points)
    print(f"Scale factor used: {factor}, Number of polygons: {len(polygons.geoms)}")

    for idx, polygon in enumerate(polygons.geoms):
        plotter.plot_polygon(polygons.envelope, axes[factor_idx][idx], color="lightgray", alpha=0.5)
        plotter.plot_polygon(polygon, axes[factor_idx][idx])
    for ax in axes[factor_idx]:
        ax.set_aspect('equal')
        for center in scaled_centers:
            plotter.plot_points(shapely.Point(center[0]), color="red", ax=ax)

    for polygon in polygons.geoms:
        plotter.plot_polygon(polygon, axes[factor_idx][-1])

plt.show()
