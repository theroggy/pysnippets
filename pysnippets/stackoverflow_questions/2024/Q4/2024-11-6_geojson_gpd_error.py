"""
from osgeo import gdal

gdal.UseExceptions()
path = "C:\Temp\gras\Permanent_Grassland.geojson"
gdal.VectorTranslate(srcDS=str(path), destNameOrDestDS="C:/Temp/gras/Permanent_Grassland.gpkg")
"""

import geopandas as gpd
import pyogrio

path = "C:\Temp\gras\Permanent_Grassland.geojson"
pyogrio.set_gdal_config_options({"OGR_GEOJSON_MAX_OBJ_SIZE": 0})
gdf = gpd.read_file(path)
print(gdf)
