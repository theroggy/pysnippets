import geopandas as gpd
from osgeo import gdal

options = gdal.VectorTranslateOptions(makeValid=True)
gdal.VectorTranslate(
    srcDS="C:/Temp/invalid_shp/invalid_poly.shp",
    destNameOrDestDS="C:/Temp/invalid_shp/invalid_poly_fixed.gpkg",
    options=options,
)

# Load GIS-VMRDH-Areas with pyogrio engine
areas = gpd.read_file("C:/Temp/invalid_shp/invalid_poly_fixed.gpkg", engine="pyogrio")
print(areas)
