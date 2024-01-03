import geopandas as gpd
from matplotlib import pyplot as plt
import shapely

multiline = shapely.MultiLineString([[(0, 0), (5, 0), (10, 10)], [(5, 0), (10, -10)]])

multiline_gdf = gpd.GeoDataFrame(geometry=[multiline])
lines_gdf = multiline_gdf.explode()

multiline_gdf.plot(color="red")
lines_gdf.plot(color=["blue", "green"])
plt.show()
