from matplotlib import pyplot as plt
import shapely
import shapely.plotting as plotter

# Prepare test data
input_wkt = "MULTILINESTRING ((0 10, 10 10, 10 5), (10 10, 11 0, 10 0))"
input_geom = shapely.from_wkt(input_wkt)

# Simplify the input
result = shapely.simplify(input_geom, tolerance=1, preserve_topology=True)

# Plot input and result
fig, ax = plt.subplots(ncols=2)
colors = ["red", "blue"]
for index, line in enumerate(input_geom.geoms):
    plotter.plot_line(line, ax=ax[0], add_points=True, color=colors[index])
    ax[0].set_aspect("equal")
for index, line in enumerate(result.geoms):
    plotter.plot_line(line, ax=ax[1], add_points=True, color=colors[index])
    ax[1].set_aspect("equal")

plt.show()
