from osgeo import gdal, ogr

ogr.UseExceptions()

src_ds = ogr.GetDriverByName("MEM").CreateDataSource("")
src_lyr = src_ds.CreateLayer("src_lyr", geom_type=ogr.wkbNone)

field = ogr.FieldDefn("time", ogr.OFTTime)
src_lyr.CreateField(field)
field = ogr.FieldDefn("name", ogr.OFTString)
src_lyr.CreateField(field)

f = ogr.Feature(src_lyr.GetLayerDefn())
f.SetField("name", "row_1")
src_lyr.CreateFeature(f)

f = ogr.Feature(src_lyr.GetLayerDefn())
f.SetField("name", "row_2")
f.SetField("time", "12:34:56.789")
src_lyr.CreateFeature(f)

f = ogr.Feature(src_lyr.GetLayerDefn())
f.SetField("name", "row_3")
f.SetField("time", "12:34:56")
src_lyr.CreateFeature(f)

output_path = "C:/temp/test.geojson"
ds = ogr.GetDriverByName("GeoJSON").CreateDataSource(output_path)
dst_lyr = ds.CreateLayer("dst_lyr")

stream = src_lyr.GetArrowStream()
schema = stream.GetSchema()

for i in range(schema.GetChildrenCount()):
    dst_lyr.CreateFieldFromArrowSchema(schema.GetChild(i))

while True:
    array = stream.GetNextRecordBatch()
    if array is None:
        break
    dst_lyr.WriteArrowBatch(schema, array)

dst_lyr = None
ds = None

# List fields in dst_lyr to verify correctness
ds = ogr.Open(output_path, gdal.OF_VECTOR | gdal.OF_READONLY)
dst_lyr = ds.GetLayer()
layer_defn = dst_lyr.GetLayerDefn()
for i in range(layer_defn.GetFieldCount()):
    name = layer_defn.GetFieldDefn(i).GetName()
    # TODO: think whether the type name should be converted to other names
    gdal_type = layer_defn.GetFieldDefn(i).GetTypeName()

    print(f"Field {i}: name={name}, type={gdal_type}")

for feat in dst_lyr:
    name = feat.GetFieldAsString("name")
    time = feat.GetFieldAsString("time")
    print(f"Feature: name={name}, time={time}")
