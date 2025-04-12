from osgeo import ogr

ogr.UseExceptions()

src_ds = ogr.GetDriverByName("Memory").CreateDataSource("")
src_lyr = src_ds.CreateLayer("src_lyr", geom_type=ogr.wkbNone)

field = ogr.FieldDefn("dt", ogr.OFTDateTime)
src_lyr.CreateField(field)

f = ogr.Feature(src_lyr.GetLayerDefn())
src_lyr.CreateFeature(f)

f = ogr.Feature(src_lyr.GetLayerDefn())
f.SetField("dt", "2022-05-31T12:34:56.789Z")
src_lyr.CreateFeature(f)

ds = ogr.GetDriverByName("GPKG").CreateDataSource("C:/Temp/test.gpkg.zip")
dst_lyr = ds.CreateLayer("dst_lyr")

stream = src_lyr.GetArrowStream(["DATETIME_AS_STRING=YES"])
schema = stream.GetSchema()

for i in range(schema.GetChildrenCount()):
    dst_lyr.CreateFieldFromArrowSchema(schema.GetChild(i))

while True:
    array = stream.GetNextRecordBatch()
    if array is None:
        break
    dst_lyr.WriteArrowBatch(schema, array)
