import os

os.system("""
    ogr2ogr -f CSV output_points.csv "C:/Temp/polygon_parcel/polygon-parcel_polygonized.shp" -dialect SQLite -sql "SELECT ST_X(geom) AS X, ST_Y(geom) AS Y FROM (SELECT ST_DumpPoints(geometry) FROM [polygon-parcel_polygonized])"
"""
)