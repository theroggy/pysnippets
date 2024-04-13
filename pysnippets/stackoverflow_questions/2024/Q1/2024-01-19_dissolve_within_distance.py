from pathlib import Path
import geofileops as gfo
import geopandas as gpd
from matplotlib import pyplot as plt
from shapely import Polygon

# Prepare input
p1 = Polygon([(0, 0), (10, 0), (10, 9.8), (0, 9.8)])
p2 = Polygon([(10.2, 10), (20, 10), (20, 20), (10.2, 20)])
p3 = Polygon([(10, 10), (9.8, 20), (0, 10)])
df = gpd.GeoDataFrame(geometry=[p1, p2, p3])
input_path = Path("input.gpkg")
df.to_file("input.gpkg")

# Process
output_path = Path("output.gpkg")
gfo.dissolve_within_distance(input_path, output_path, distance=1, gridsize=0.0)

# Visualize
result_df = gpd.read_file("output.gpkg")
ax = result_df.plot(color="green")
df.plot(ax=ax, edgecolor="blue", facecolor="none")
plt.show()
