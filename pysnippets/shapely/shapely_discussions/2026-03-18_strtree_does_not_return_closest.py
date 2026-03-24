import matplotlib.pyplot as plt
import osmnx as ox
from shapely.geometry import Point
from shapely.strtree import STRtree
from shapely import plotting

G = ox.graph_from_place("Bern, Switzerland",
    custom_filter='["railway"~"tram"]',
    network_type="all"
)
G = ox.project_graph(G)
gps_point = Point([381365.3297120359, 5200530.156074275])
geometries = [data["geometry"] for u, v, data in G.edges(data=True) if "geometry" in data]
tree = STRtree(geometries)
idxs = tree.query(gps_point.buffer(5))
print(idxs)
idxs_fix = tree.query_nearest(gps_point.buffer(5))
print(idxs_fix)

# Plot
for idx, geom in enumerate(geometries):
    plotting.plot_line(geom, color="blue")
    plotting.plot_polygon(geom.envelope, color="grey")
    if idx in idxs:
        plotting.plot_line(geom, color="orange")
plotting.plot_polygon(gps_point.buffer(5), color="red", add_points=False)
plotting.plot_line(geometries[idxs_fix[0]], color="green")
plotting.plot_points([gps_point], color="black")
plt.show()
