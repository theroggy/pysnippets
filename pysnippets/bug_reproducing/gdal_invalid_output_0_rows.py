from osgeo import gdal

gdal.UseExceptions()

# Cannot be reproduced anymore in gdal 3.7.0

# Paths
src = "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"
# dst = "C:/temp/dst2.gpkg"
dst = "C:/temp/dst2.shp"

# Run test
sql = "SELECT * FROM parcels WHERE 1 = 0"
options = gdal.VectorTranslateOptions(SQLStatement=sql, layerName="parcels")
ds_output = gdal.VectorTranslate(srcDS=src, destNameOrDestDS=dst, options=options)

# Print some properties of output file
ds_layer = ds_output.GetLayerByIndex(0)
geometrytype = gdal.ogr.GeometryTypeToName(ds_layer.GetGeomType())
print(f"geometrycolumn: {ds_layer.GetGeometryColumn()}, type: {geometrytype}")
spatialref = ds_layer.GetSpatialRef()
if spatialref is not None:
    print(f"spatialref: {spatialref.ExportToWkt()}")
else:
    print("spatialref is None")
layer_defn = ds_layer.GetLayerDefn()
for i in range(layer_defn.GetFieldCount()):
    name = layer_defn.GetFieldDefn(i).GetName()
    gdal_type = layer_defn.GetFieldDefn(i).GetTypeName()
    print(f"column: {name}, type: {gdal_type}")

ds_output = None
