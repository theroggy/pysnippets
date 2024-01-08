import geopandas as gpd
from matplotlib import pyplot as plt
import shapely

# Prepare input
line = shapely.LineString([(-1, 0), (2, 0)])
multiline = shapely.MultiLineString([[(2, 0), (5, 0), (10, 10)], [(5, 0), (10, -10)]])
lines_gdf = gpd.GeoDataFrame(geometry=[line, multiline])

# Apply union + explode: touching lines stay seperate
lines_union = lines_gdf.unary_union
print(lines_union)
lines_union_gdf = gpd.GeoDataFrame(geometry=[lines_union]).explode(ignore_index=True)

# Apply union + line_merge + explode: touching lines are merged
lines_merged = shapely.line_merge(lines_gdf.unary_union)
print(lines_merged)
lines_merged_gdf = gpd.GeoDataFrame(geometry=[lines_merged]).explode(ignore_index=True)

# Plot
lines_gdf.plot(color=["orange", "red"])
lines_union_gdf.plot(color=["orange", "red", "green", "yellow"])
lines_merged_gdf.plot(color=["blue", "green", "yellow"])
plt.show()
