import tempfile
from pathlib import Path

from osgeo import ogr

ogr.UseExceptions()

temp_dir = Path(tempfile.gettempdir())
parquet_driver = ogr.GetDriverByName("Parquet")
if parquet_driver is None:
    raise RuntimeError("The GDAL build does not provide the Parquet driver")

# Write parquet with classic mode
# -------------------------------
parquet_classic_output_path = str(temp_dir / "test_classic.parquet")
classic_ds = parquet_driver.CreateDataSource(parquet_classic_output_path)
classic_lyr = classic_ds.CreateLayer("dst_lyr", geom_type=ogr.wkbNone)

field = ogr.FieldDefn("dt", ogr.OFTDateTime)
classic_lyr.CreateField(field)

field = ogr.FieldDefn("str", ogr.OFTString)
field.SetWidth(10)
classic_lyr.CreateField(field)

f = ogr.Feature(classic_lyr.GetLayerDefn())
classic_lyr.CreateFeature(f)

f = ogr.Feature(classic_lyr.GetLayerDefn())
f.SetField("dt", "2022-05-31T12:34:56.789Z")
f.SetField("str", "value")
classic_lyr.CreateFeature(f)

classic_ds = None
classic_check_ds = ogr.Open(parquet_classic_output_path)
classic_check_lyr = classic_check_ds.GetLayer(0)
field_index = classic_check_lyr.GetLayerDefn().GetFieldIndex("str")
assert field_index >= 0, "The classic Parquet file is missing the string field"
classic_written_width = (
    classic_check_lyr.GetLayerDefn().GetFieldDefn(field_index).GetWidth()
)
print(f"Classic write Parquet, string field width: {classic_written_width}, expected 10")
field_index = classic_check_lyr.GetLayerDefn().GetFieldIndex("dt")
assert field_index >= 0, "The classic Parquet file is missing the datetime field"
datetime_type = classic_check_lyr.GetLayerDefn().GetFieldDefn(field_index).GetTypeName()
print(f"Classic write Parquet, datetime field type: {datetime_type}, expected DateTime")

# Write Parquet file using batch Arrow stream
# -------------------------------------------
parquet_batch_output_path = str(temp_dir / "test.parquet")

src_ds = ogr.GetDriverByName("MEM").CreateDataSource("")
src_lyr = src_ds.CreateLayer("src_lyr", geom_type=ogr.wkbNone)

field = ogr.FieldDefn("dt", ogr.OFTDateTime)
src_lyr.CreateField(field)

field = ogr.FieldDefn("str", ogr.OFTString)
field.SetWidth(10)
src_lyr.CreateField(field)

f = ogr.Feature(src_lyr.GetLayerDefn())
src_lyr.CreateFeature(f)

f = ogr.Feature(src_lyr.GetLayerDefn())
f.SetField("dt", "2022-05-31T12:34:56.789Z")
f.SetField("str", "value")
src_lyr.CreateFeature(f)

ds = parquet_driver.CreateDataSource(parquet_batch_output_path)
dst_lyr = ds.CreateLayer("dst_lyr", geom_type=ogr.wkbNone)

stream = src_lyr.GetArrowStream(["DATETIME_AS_STRING=YES"])
schema = stream.GetSchema()

for i in range(schema.GetChildrenCount()):
    dst_lyr.CreateFieldFromArrowSchema(schema.GetChild(i))

while True:
    array = stream.GetNextRecordBatch()
    if array is None:
        break
    dst_lyr.WriteArrowBatch(schema, array)

ds = None
check_ds = ogr.Open(parquet_batch_output_path)
check_lyr = check_ds.GetLayer(0)
field_index = check_lyr.GetLayerDefn().GetFieldIndex("str")
assert field_index >= 0, "The written Parquet file is missing the string field"
written_width = check_lyr.GetLayerDefn().GetFieldDefn(field_index).GetWidth()
print(f"Arrow batch write Parquet, string field width: {written_width}, expected 10")
field_index = check_lyr.GetLayerDefn().GetFieldIndex("dt")
assert field_index >= 0, "The Arrow-written Parquet file is missing the datetime field"
datetime_type = check_lyr.GetLayerDefn().GetFieldDefn(field_index).GetTypeName()
print(f"Arrow batch write Parquet, datetime field type: {datetime_type}, expected DateTime")

# Write GPKG file using batch Arrow stream
# -------------------------------------------
gpkg_batch_output_path = str(temp_dir / "test.gpkg")
gpkg_driver = ogr.GetDriverByName("GPKG")
if gpkg_driver is None:
    raise RuntimeError("The GDAL build does not provide the GPKG driver")

src_ds = ogr.GetDriverByName("MEM").CreateDataSource("")
src_lyr = src_ds.CreateLayer("src_lyr", geom_type=ogr.wkbNone)

field = ogr.FieldDefn("dt", ogr.OFTDateTime)
src_lyr.CreateField(field)

field = ogr.FieldDefn("str", ogr.OFTString)
field.SetWidth(10)
src_lyr.CreateField(field)

f = ogr.Feature(src_lyr.GetLayerDefn())
src_lyr.CreateFeature(f)

f = ogr.Feature(src_lyr.GetLayerDefn())
f.SetField("dt", "2022-05-31T12:34:56.789Z")
f.SetField("str", "value")
src_lyr.CreateFeature(f)

ds = gpkg_driver.CreateDataSource(gpkg_batch_output_path)
dst_lyr = ds.CreateLayer("dst_lyr", geom_type=ogr.wkbNone)

stream = src_lyr.GetArrowStream(["DATETIME_AS_STRING=YES"])
schema = stream.GetSchema()

for i in range(schema.GetChildrenCount()):
    dst_lyr.CreateFieldFromArrowSchema(schema.GetChild(i))

while True:
    array = stream.GetNextRecordBatch()
    if array is None:
        break
    dst_lyr.WriteArrowBatch(schema, array)

ds = None
check_ds = ogr.Open(gpkg_batch_output_path)
check_lyr = check_ds.GetLayer(0)
field_index = check_lyr.GetLayerDefn().GetFieldIndex("str")
assert field_index >= 0, "The written GPKG file is missing the string field"
written_width = check_lyr.GetLayerDefn().GetFieldDefn(field_index).GetWidth()
print(f"Arrow batch write GPKG, string field width: {written_width}, expected 10")
field_index = check_lyr.GetLayerDefn().GetFieldIndex("dt")
assert field_index >= 0, "The Arrow-written GPKG file is missing the datetime field"
datetime_type = check_lyr.GetLayerDefn().GetFieldDefn(field_index).GetTypeName()
print(f"Arrow batch write GPKG, datetime field type: {datetime_type}, expected DateTime")
