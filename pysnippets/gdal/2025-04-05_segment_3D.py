from osgeo import gdal

with open('input.csv', 'w') as f:
    f.write("WKT\n")
    f.write('"LINESTRING Z (0 0 0, 8 8 8)\n"')

gdal.UseExceptions()
options = gdal.VectorTranslateOptions(
    format='CSV',
    layerCreationOptions=['GEOMETRY=AS_WKT', 'GEOMETRY_NAME=WKT'],
    SQLStatement='SELECT geometry AS WKT FROM input',
    SQLDialect='SQLite',
    segmentizeMaxDist=3,
)
gdal.VectorTranslate('output.csv', 'input.csv', options=options)
#ogr2ogr n.csv m.csv -lco GEOMETRY=AS_WKT -dialect SQLite \
# -sql 'SELECT geometry AS WKT FROM "m"' -segmentize 3