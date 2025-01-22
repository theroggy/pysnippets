import os
import tempfile
from pathlib import Path
from osgeo import gdal, ogr

ogr.UseExceptions()

# Create input test file with a datetime field with a date in it
tmp_dir = Path(tempfile.gettempdir())
input_path = tmp_dir / "test.gpkg"
input_path.unlink(missing_ok=True)
src_ds = ogr.GetDriverByName("GPKG").CreateDataSource(input_path)
src_lyr = src_ds.CreateLayer("src_lyr")

field_def = ogr.FieldDefn("field_int", ogr.OFTInteger)
src_lyr.CreateField(field_def)

field_def = ogr.FieldDefn("field_dt", ogr.OFTDateTime)
src_lyr.CreateField(field_def)

field_def = ogr.FieldDefn("field_date", ogr.OFTDate)
src_lyr.CreateField(field_def)

feat_def = src_lyr.GetLayerDefn()
src_feature = ogr.Feature(feat_def)
src_feature.SetField("field_int", 1)

#src_feature.SetField("field_dt", "2020-05-01")
#src_feature.SetField("field_dt", "2020-05-01T00:00:00.000Z")
#src_feature.SetField("field_dt", "2020-05-01T01:02:03.456Z")
src_feature.SetField("field_dt", "2020-05-01T01:02:03.456+10:00")
src_feature.SetField("field_date", "2020-05-01")

src_feature.SetGeometry(ogr.CreateGeometryFromWkt("POINT (1 2)"))
src_feature.SetFID(1)

src_lyr.CreateFeature(src_feature)

src_ds = None

# Translate the file to a new shapefile, without arrow API: datetime becomes date
print("=== output file info, WITHOUT arrow ===")
output_path = tmp_dir / "test_noarrow.shp"
os.environ["OGR2OGR_USE_ARROW_API"] = "NO"
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path)
output_ds = None

output_ds = gdal.OpenEx(output_path, nOpenFlags=gdal.OF_VECTOR)
output_layer = output_ds.GetLayer()
layer_defn = output_layer.GetLayerDefn()
print(f'{layer_defn.GetFieldDefn(1).GetName()} type: {layer_defn.GetFieldDefn(1).GetTypeName()}')
print(f'{layer_defn.GetFieldDefn(2).GetName()} type: {layer_defn.GetFieldDefn(2).GetTypeName()}')

# Translate the file to a new shapefile, with arrow API: datetime becomes string
print("=== output file info, WITH arrow ===")
output_path = tmp_dir / "test_arrow.shp"
os.environ["OGR2OGR_USE_ARROW_API"] = "YES"
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path)
output_ds = None

output_ds = gdal.OpenEx(output_path, nOpenFlags=gdal.OF_VECTOR)
output_layer = output_ds.GetLayer()
layer_defn = output_layer.GetLayerDefn()
print(f'{layer_defn.GetFieldDefn(1).GetName()} type: {layer_defn.GetFieldDefn(1).GetTypeName()}')
print(f'{layer_defn.GetFieldDefn(2).GetName()} type: {layer_defn.GetFieldDefn(2).GetTypeName()}')

"""
# Translate the file to a new shapefile
prc_path = "C:/Temp/polygon-parcel_31370_None.gpkg"
prc_out_path = "C:/Temp/polygon-parcel_31370_None.shp"
prc_out_ds = gdal.VectorTranslate(destNameOrDestDS=prc_out_path, srcDS=prc_path)
prc_out_ds = None

print("=== output prc file info ===")
prc_out_ds = gdal.OpenEx(prc_out_path, nOpenFlags=gdal.OF_VECTOR)
prc_output_layer = prc_out_ds.GetLayer()
layer_defn = prc_output_layer.GetLayerDefn()
print(f'{layer_defn.GetFieldDefn("DATUM").GetName()} type: {layer_defn.GetFieldDefn("DATUM").GetTypeName()}')
"""
