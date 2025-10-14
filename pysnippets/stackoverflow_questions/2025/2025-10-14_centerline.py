"""
This script reads a raster image, polygonizes it and calculates the centerline of the
polygons.

Ref: https://gis.stackexchange.com/questions/495732/skeletonize-or-extract-lines-from-segmentation-image
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pygeoops
import shapely
import rasterio as rio
from rasterio import features

# Polygonize the image.
path = "https://i.sstatic.net/M5kSIlpB.png"
with rio.open(path) as src:
    image = src.read(1)

    # Flip image vertically to get the result like in the example.
    image = image[::-1, :]
    polygons = []
    for coords, value in features.shapes(image, image > 0):
        polygons.append(shapely.geometry.shape(coords))

    gdf = gpd.GeoDataFrame(geometry=polygons, crs=src.crs)

# Calculate the centerline.
centerlines_gdf = gdf.copy()
centerlines_gdf["geometry"] = pygeoops.centerline(gdf["geometry"])

print(centerlines_gdf)
centerlines_gdf.plot()
plt.show()
