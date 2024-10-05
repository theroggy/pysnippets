import geopandas as gpd
import shapely
from matplotlib import pyplot as plt
from matplotlib.colors import BASE_COLORS
from shapely.geometry import Polygon, LineString
from shapely.plotting import plot_line


gdf1 = gpd.GeoDataFrame({
  'geom': [
    Polygon(((32, 41), (34, 44), (36, 42), (32, 41))),
    Polygon(((34, 44), (36, 42), (37, 44), (34, 44))),
    Polygon(((36, 42), (37, 41), (37, 44), (36, 42))),
    Polygon(((37, 44), (39, 46), (40, 42), (37, 44))),
    Polygon(((37, 44), (40, 42), (37, 41), (37, 44))),
    Polygon(((37, 41), (36, 40), (36, 42), (37, 41))),
    Polygon(((36, 40), (32, 41), (36, 42), (36, 40))),
    Polygon(((37, 44), (36, 46), (34, 44), (37, 44))),
    Polygon(((36, 46), (39, 46), (37, 44), (36, 46))),
  ]}, geometry='geom', crs=2056
)

gdf2 = gpd.GeoDataFrame({
  'geom': [
    LineString(((33.0204, 39.937), (35.429, 40.534), (35.795, 41.170), (37.183, 41.691), (37.954, 42.365), (38.262, 43.849), (40.112, 45.661))),
    LineString(((38.2624, 43.849), (37.183, 43.406), (36.258, 43.406), (35.352, 43.772), (34.118, 43.387), (33.116, 42.288), (31.575, 41.806))),
    LineString(((35.3523, 43.772), (37.048, 45.198), (38.802, 46.316))),
    LineString(((32.2302, 40.554), (33.868, 41.113), (34.408, 42.365), (35.352, 43.772)))
  ]}, geometry='geom', crs=2056
)
print(f"{len(gdf2)=}, with respectively {list(shapely.get_num_coordinates(gdf2.geometry))} coordinates")

gdf3 = gdf2.overlay(gpd.GeoDataFrame(geometry=gdf1.boundary, crs=gdf1.crs), how='difference', keep_geom_type=False)

print(f"{len(gdf3)=}, with respectively {list(shapely.get_num_coordinates(gdf3.geometry))} coordinates")

for i in range(len(gdf3)):
  plot_line(gdf3.geometry[i], color=list(BASE_COLORS)[i])
plt.show()
