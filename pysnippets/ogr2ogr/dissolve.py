"""
Stackoverflow question:
https://gis.stackexchange.com/questions/481099/error-in-dissolving-shapefile-with-ogr2ogr
"""

import os

os.system(
    r'ogr2ogr -dialect sqlite -sql "SELECT ST_Union(geometry) AS geometry FROM ""93000100_qk21_new""" "C:\Temp\polygon_parcel\93000100_qk21_new_1.shp" "C:\Temp\polygon_parcel\93000100_qk21_new.shp"'
)

# Command standalone:
# ogr2ogr -dialect sqlite -sql "SELECT ST_Union(geometry) AS geometry FROM ""93000100_qk21_new""" 93000100_qk21_new_1.shp 93000100_qk21_new.shp
