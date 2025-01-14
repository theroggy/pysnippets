import os
from pathlib import Path
from osgeo import gdal, ogr

ogr.UseExceptions()

# Create input test file with a datetime field with a date in it
input_path = "C:/temp/test.gpkg"
Path(input_path).unlink(missing_ok=True)
src_ds = ogr.GetDriverByName("GPKG").CreateDataSource(input_path)
src_lyr = src_ds.CreateLayer("src_lyr")

field_def = ogr.FieldDefn("field_int", ogr.OFTInteger)
src_lyr.CreateField(field_def)

field_def = ogr.FieldDefn("field_date", ogr.OFTDateTime)
src_lyr.CreateField(field_def)

feat_def = src_lyr.GetLayerDefn()
src_feature = ogr.Feature(feat_def)
src_feature.SetField("field_int", 1)
src_feature.SetField("field_date", "2014-12-04")
src_feature.SetGeometry(ogr.CreateGeometryFromWkt("POINT (1 2)"))
src_feature.SetFID(1)

src_lyr.CreateFeature(src_feature)

src_ds = None

# Translate the file to a new shapefile, with arrow API: datetime becomes string
output_path = "C:/temp/test_arrow.shp"
os.environ["OGR2OGR_USE_ARROW_API"] = "YES"
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path)
output_ds = None

print("=== output file info, without arrow ===")
output_ds = gdal.OpenEx(output_path, nOpenFlags=gdal.OF_VECTOR)
output_layer = output_ds.GetLayer()
layer_defn = output_layer.GetLayerDefn()
print(f'{layer_defn.GetFieldDefn(1).GetName()} type: {layer_defn.GetFieldDefn(1).GetTypeName()}')

# Translate the file to a new shapefile, without arrow API: datetime becomes date
output_path = "C:/temp/test_noarrow.shp"
os.environ["OGR2OGR_USE_ARROW_API"] = "NO"
output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path)
output_ds = None

print("=== output file info, without arrow ===")
output_ds = gdal.OpenEx(output_path, nOpenFlags=gdal.OF_VECTOR)
output_layer = output_ds.GetLayer()
layer_defn = output_layer.GetLayerDefn()
print(f'{layer_defn.GetFieldDefn(1).GetName()} type: {layer_defn.GetFieldDefn(1).GetTypeName()}')

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
