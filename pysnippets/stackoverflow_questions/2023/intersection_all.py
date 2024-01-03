import geopandas as gpd
from matplotlib import pyplot as plt
import shapely
import shapely.plotting

data = [
    {"geometry": shapely.box(0, 0, 100, 100), "color": "blue"},
    {"geometry": shapely.box(50, 50, 150, 150), "color": "green"},
    {"geometry": shapely.box(25, 75, 75, 125), "color": "yellow"},
]

data_gdf = gpd.GeoDataFrame(data)
result = shapely.intersection_all(data_gdf.geometry)
print(result)

data_gdf.plot(color=data_gdf["color"], alpha=0.50)
shapely.plotting.plot_polygon(result, color="red", linewidth=2)
plt.show()
