import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

import shapely
import shapely.ops
import shapely.plotting as plotter

print(f"{shapely.__version__=}")
print(f"{shapely.geos_version_string=}")

polygon = shapely.Polygon([(0.0, 0.0), (0.0, 50), (1, 50), (1, 1), (49, 1), (49, 50), (50, 50), (50, 0.0), (0.0, 0.0)])
split_line = shapely.LineString([[0,1.000000000000652],[51.005,1.000000000000652]])

result = shapely.ops.split(polygon, split_line)
print(result)

fig, ax = plt.subplots()
plotter.plot_polygon(polygon, ax=ax, color="blue")
plotter.plot_line(split_line, ax=ax, color="red")
for idx, geom in enumerate(result.geoms):
    plotter.plot_polygon(geom, ax=ax, color=list(mcolors.TABLEAU_COLORS.keys())[idx])
plt.show()
