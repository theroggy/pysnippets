# https://stackoverflow.com/questions/78919389/merging-one-kml-with-multiple-polygons-with-another-kml-with-multiple-polygons-t

import geopandas as gpd
from matplotlib import pyplot as plt
import pandas as pd
from shapely import box


# Normally... read kml files, but for this sample script, create sample data.
# file1_gdf = gpd.read_file("test1.kml", driver="kml")
file1_gdf = gpd.GeoDataFrame(geometry=[box(0, 0, 10, 10), box(20, 0, 30, 10)])
# file2_gdf = gpd.read_file("test2.kml", driver="kml")
file2_gdf = gpd.GeoDataFrame(geometry=[box(5, 5, 15, 15), box(20, 15, 25, 20)])

# Find overlapping polygons, in both directions.
file1_overlapping_gdf = file1_gdf.sjoin(file2_gdf, how="inner")
file2_overlapping_gdf = file2_gdf.sjoin(file1_gdf, how="inner")

# Concat both results and merge/dissolve the overlapping polygons.
overlapping_gdf = pd.concat([file1_overlapping_gdf, file2_overlapping_gdf])
dissolved_overlapping_gdf = overlapping_gdf.dissolve()

# Plot input and result.
ax = file1_gdf.plot(color="blue", alpha=0.2)
file2_gdf.plot(color="green", ax=ax, alpha=0.2)
dissolved_overlapping_gdf.plot(ax=ax, facecolor="none", edgecolor="red", hatch="/")
plt.show()
