from matplotlib import pyplot as plt
import numpy as np

import rasterio
import rasterio.plot
from rasterio import features
import shapely
from shapely.plotting import plot_polygon

path = "http://download.osgeo.org/geotiff/samples/other/erdas_spnad83.tif"
value_to_keep = 0

result = []
with rasterio.open(path) as src:
    image = src.read(1)

    # create a binary image, 1 where value is value_to_keep, 0 for the rest
    is_valid = (image != value_to_keep).astype(np.uint8)

    # vectorize the binary image, supplying the transform so it returns map coords
    for coords, value in features.shapes(is_valid, transform=src.transform):
        # only keep polygons corresponding to value_to_keep
        if value == value_to_keep:
            # convert geojson to shapely geometry
            result.append(shapely.geometry.shape(coords))

    # Plot result
    fig, ax = plt.subplots()
    ax = rasterio.plot.show(image, ax=ax, transform=src.transform, cmap="Greys_r")

    for geom in result:
        plot_polygon(geom, ax=ax, color="grey", add_points=False, hatch="/")
    plt.show()
