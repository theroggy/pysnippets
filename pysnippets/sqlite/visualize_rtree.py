from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import shapely

path = Path("C:/Temp/polygon-parcel.gpkg")
df = gpd.read_file(path, layer="bboxes_rtree_node_bulk", ignore_geometry=True)
boxes = shapely.box(xmin=df.minx, ymin=df.miny, xmax=df.maxx, ymax=df.maxy)

gdf = gpd.GeoDataFrame(df, geometry=boxes).query("level > 0").sort_values("level")
gdf["color"] = "yellow"
gdf.loc[gdf["level"] == 2, "color"] = "green"
gdf.loc[gdf["level"] == 3, "color"] = "blue"
gdf.plot(facecolor="none", edgecolor=gdf["color"])
plt.show()

