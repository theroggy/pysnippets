import geopandas as gpd
from matplotlib import pyplot as plt
import shapely

# Source layer
data = [
    {"geometry": shapely.box(0, 0, 100, 100), "color": "blue"},
    {"geometry": shapely.box(50, 50, 150, 150), "color": "green"},
    {"geometry": shapely.box(25, 75, 75, 125), "color": "yellow"},
]
data_gdf = gpd.GeoDataFrame(data)

# Overlaps check
union_gdf = data_gdf.overlay(data_gdf, how="union")
# union_gdf = union_gdf.loc[union_gdf.color_1 != union_gdf.color_2]

print(union_gdf)
data_gdf.plot(color=data_gdf["color"], alpha=0.50)
union_gdf.plot(color=union_gdf["color_1"], alpha=0.50)
plt.show()
