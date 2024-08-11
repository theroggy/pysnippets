import geopandas as gpd
import rasterio
from rasterio import features

src = r"C:\Temp\polygon_parcel\polygon-parcel.tif"
output = r"C:\Temp\polygon_parcel\polygon-parcel_polygonized_rio.shp"

result = []
with rasterio.open(src) as srcfile:
    # Vectorize.
    ds_features = features.dataset_features(srcfile, bidx=1, geographic=False)
    gdf = gpd.GeoDataFrame.from_features(ds_features, crs=srcfile.crs)

gdf.to_file(output)
