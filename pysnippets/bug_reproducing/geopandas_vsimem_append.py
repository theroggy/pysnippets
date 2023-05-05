import pyogrio
import geopandas as gpd
from osgeo import gdal

gdf = gpd.GeoDataFrame(gpd.read_file(gpd.datasets.get_path("nybb")))

memfile_path = "/vsimem/memoryfile.gpkg"
# memfile_path = "C:/temp/memoryfile.gpkg"
try:
    gdf.iloc[[0, 1]].to_file(memfile_path, driver="GPKG", layer="test1" , engine="pyogrio")
    layers = pyogrio.list_layers(memfile_path)
    gdf.iloc[[2, 3]].to_file(memfile_path, driver="GPKG", layer="test2" , engine="pyogrio")
    layers = pyogrio.list_layers(memfile_path)
    print(layers)
    gdf1 = gpd.read_file(memfile_path, driver="GPKG", layer="test1")
    gdf2 = gpd.read_file(memfile_path, driver="GPKG", layer="test2")
    print(gdf1)
    print(gdf2)
finally:
    gdal.Unlink(memfile_path)