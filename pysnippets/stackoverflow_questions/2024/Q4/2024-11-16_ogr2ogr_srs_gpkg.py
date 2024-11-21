import os

input = r"C:\Temp\polygon_parcel\polygon_parcel_polygonized_noproj\polygon-parcel_polygonized.shp"
output = r"C:\Temp\polygon_parcel\polygon_parcel_polygonized_noproj\polygon-parcel_polygonized_proj.gpkg"
os.system(f'ogr2ogr -f GPKG -nlt POINT -a_srs EPSG:20355 "{output}" "{input}"')
