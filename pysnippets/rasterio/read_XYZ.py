import math
import numpy as np
import geopandas as gpd
import rasterio as rio
from shapely import box

roi = gpd.GeoDataFrame(geometry=[box(150000, 150000, 154000, 154000)], crs=31370).to_crs(
    3857
)
west, south, east, north = roi.total_bounds

layer = rio.open("rasterio/layers/XYZ_topo.xml")
# Calculate the pixel positions of the desired bounding box at the highest zoom level
# as specified in the XML file.


#bl = layer.index(west, south, op=math.floor)
#tr = layer.index(east, north, op=math.ceil)
bl = (west, south)
tr = (east, north)
# image_size is a tuple (h, w, num_bands)
image_size = (512, 512, 3)
output_dataset = np.empty(shape=image_size, dtype=layer.profile["dtype"])

# Read each band
layer.read(1, out=output_dataset[:, :, 0], window=((tr[0], bl[0]), (bl[1], tr[1])))
layer.read(2, out=output_dataset[:, :, 1], window=((tr[0], bl[0]), (bl[1], tr[1])))
layer.read(3, out=output_dataset[:, :, 2], window=((tr[0], bl[0]), (bl[1], tr[1])))

# Create an output image dataset
output_image = rio.open(
    "output/read_XYZ_topo_output.png",
    "w",
    driver="png",
    width=image_size[1],
    height=image_size[0],
    count=3,
    dtype=output_dataset.dtype,
)
# Write each band
output_image.write(output_dataset[:, :, 0], 1)
output_image.write(output_dataset[:, :, 1], 2)
output_image.write(output_dataset[:, :, 2], 3)

output_image.close()
