"""
Stackoverflow question:
https://gis.stackexchange.com/questions/490023/how-to-set-spatialite-global-settings-in-gdal-ogr/490034#490034
"""
import geopandas as gpd
import os

# SetDecimalPrecision function is not available in prelude_statements
cmd = '''ogr2ogr -dialect sqlite -oo PRELUDE_STATEMENTS="SELECT enable_load_extension(1);SELECT load_extension('mod_spatialite');SELECT SetDecimalPrecision(1)" -sql "SELECT * FROM \"parcels\"" "C:\Temp\polygon_parcel\polygon-parcel2.gpkg" "C:\Temp\polygon_parcel\polygon-parcel.gpkg"'''
os.system(cmd)

print(gpd.read_file("C:/Temp/polygon_parcel/polygon-parcel.gpkg"))
print(gpd.read_file("C:/Temp/polygon_parcel/polygon-parcel2.gpkg"))
