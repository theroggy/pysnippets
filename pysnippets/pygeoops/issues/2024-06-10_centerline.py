from matplotlib import pyplot as plt
import pygeoops
import shapely
import shapely.plotting

with open("c:/temp/rhin_tortu.geojson") as input:
    polygon = shapely.from_geojson(input.read()).geoms[0]

centerline_default = pygeoops.centerline(polygon)
centerline2 = pygeoops.centerline(
    polygon, densify_distance=0.00001, simplifytolerance=0.000005
)

_, ax = plt.subplots()
shapely.plotting.plot_polygon(polygon, ax=ax, color="blue", linewidth=1)
shapely.plotting.plot_line(centerline_default, ax=ax, color="red", linewidth=1)
shapely.plotting.plot_line(centerline2, ax=ax, color="green", linewidth=1)
plt.show()
