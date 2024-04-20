import geopandas as gpd
import shapely
import shapely.plotting
import matplotlib.pyplot as plt


# Test data
poly1 = shapely.Polygon([(0, 0), (0, 10), (10, 10), (5, 0), (0, 0)])
poly2 = shapely.Polygon([(5, 0), (8, 7), (10, 7), (10, 0), (5, 0)])
poly3 = shapely.Polygon([(0, 0), (5.4, 0), (5.4, 5.6), (0, 5.6), (0, 0)])

intersection_nogridsize = poly1.intersection(poly2)
gdf = gpd.GeoDataFrame(geometry=[intersection_nogridsize, poly3])
cleaned_gdf = gdf.copy()
cleaned_gdf.geometry = shapely.set_precision(cleaned_gdf.geometry, grid_size=1)

# Plot result
fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, sharex=ax1, sharey=ax1)
gdf.plot(ax=ax1)
cleaned_gdf.plot(ax=ax2)
plt.show()
