from pathlib import Path
import geopandas as gpd
from matplotlib import pyplot as plt
import numpy as np
from pyproj import CRS
import rasterio
from rasterio.plot import show
from rasterio.transform import from_origin

dir = Path(r"C:\Temp\bla")
tobacco_in_path = dir / "GDD_Count_ssp245_2020_tobacco.tif"

# Read the file in the zip file
with rasterio.open(tobacco_in_path, mode="r", driver="GTiff") as input:
    GDD_arr = input.read(1)

# Write the tiff again, using transform from the code in the post
tiff_path = dir / "GDD_Count_ssp245_2020_tobacco2.tif"
with rasterio.open(
    tiff_path,
    mode="w",
    driver="GTiff",
    height=GDD_arr.shape[0],
    width=GDD_arr.shape[1],
    count=1,
    dtype="float32",
    crs=CRS.from_epsg(4326),
    transform=from_origin(-60.875, -23.125, 0.25, 0.25),
    nodata=-9999,
) as new_dataset:
    new_dataset.write(np.flipud(GDD_arr), 1)

# Open the raster and shapefile
tiff = rasterio.open(tiff_path)
shapefile = gpd.read_file(dir / "RGdS_AgData.shp")

# set up plot
f, ax = plt.subplots()

# plot DEM with rasterio, so transform is applied
show(tiff, ax=ax)

# plot shapefiles
shapefile.plot(ax=ax, facecolor="w", edgecolor="k")
plt.show()
