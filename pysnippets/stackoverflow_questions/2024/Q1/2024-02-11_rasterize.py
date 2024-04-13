import geopandas as gpd
import rasterio
from rasterio import features
from shapely.geometry import Polygon
import rasterio.plot

# Prepare GeoDataFrame to be rasterized
geometries = [
    Polygon([(0, 5), (5, 5), (5, 0), (0, 5)]),
    Polygon([(10, 10), (10, 15), (15, 10), (10, 10)]),
]
# The waga column will be used as the burn value
data = {"waga": [1.0, 2.0]}
gdf = gpd.GeoDataFrame(data=data, geometry=geometries, crs=31370)

# Prepare some variables
xmin, ymin, xmax, ymax = gdf.total_bounds
pixel_size = 1
width = int((xmax - xmin) // pixel_size)
height = int((ymax - ymin) // pixel_size)
transform = rasterio.transform.from_origin(xmin, ymax, pixel_size, pixel_size)

# Burn geometries
shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf.waga))
burned = features.rasterize(
    shapes=shapes, out_shape=(width, height), transform=transform, all_touched=True
)

# Write result
output_path = "output.tif"
with rasterio.open(
    output_path,
    mode="w",
    driver="GTiff",
    dtype="float32",
    height=height,
    width=width,
    count=1,
    crs=gdf.crs,
    transform=transform,
    compress="lzw",
) as dest:
    dest.write_band(1, burned)

# Plot result
with rasterio.open(output_path) as src:
    image = src.read(1)
    rasterio.plot.show(image, transform=src.transform)
