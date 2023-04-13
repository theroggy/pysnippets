import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import shapely
import shapely.plotting
import matplotlib.pyplot as plt


poly1 = shapely.Polygon([(0, 0), (0, 10), (10, 10), (5, 0), (0, 0)])
poly2 = shapely.Polygon([(5, 0), (8, 7), (10, 7), (10, 0), (5, 0)])
poly3 = shapely.Polygon([(0, 0), (5.4, 0), (5.4, 5.6), (0, 5.6), (0, 0)])

intersection_nogridsize = poly1.intersection(poly2)

gdf = gpd.GeoDataFrame(geometry=[intersection_nogridsize, poly3])  # type: ignore
gdf.plot()
plt.show()

gdf.geometry.array.data = shapely.set_precision(gdf.geometry.array.data, grid_size=1)
gdf.plot()
plt.show()
