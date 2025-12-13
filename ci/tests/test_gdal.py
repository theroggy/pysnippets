import os
import tempfile
from pathlib import Path
from osgeo import gdal, ogr

ogr.UseExceptions()


def test_gdal_st_minx():
    # Create input test file with an empty geometry
    tmp_dir = Path(tempfile.gettempdir())
    input_path = tmp_dir / "test.gpkg"
    input_path.unlink(missing_ok=True)
    src_ds = ogr.GetDriverByName("GPKG").CreateDataSource(input_path)
    src_lyr = src_ds.CreateLayer("src_lyr")

    field_def = ogr.FieldDefn("field_int", ogr.OFTInteger)
    src_lyr.CreateField(field_def)

    feat_def = src_lyr.GetLayerDefn()

    src_feature = ogr.Feature(feat_def)
    src_feature.SetField("field_int", 1)
    src_feature.SetGeometry(ogr.CreateGeometryFromWkt("POLYGON ((-200 10, -190 10, -190 20, -200 20, -200 10))"))
    src_feature.SetFID(1)
    src_lyr.CreateFeature(src_feature)

    src_feature = ogr.Feature(feat_def)
    src_feature.SetField("field_int", 2)
    src_feature.SetGeometry(ogr.CreateGeometryFromWkt("POLYGON EMPTY"))
    src_feature.SetFID(2)
    src_lyr.CreateFeature(src_feature)

    src_ds = None

    # Execute an SQL statement with ST_MinX on the file
    sql_stmt = 'SELECT ST_MinX(CastToXYZ(geom)) AS minx FROM "src_lyr"'
    
    output_path = tmp_dir / "test_minx.gpkg"
    options = gdal.VectorTranslateOptions(SQLStatement=sql_stmt)
    output_ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path, options=options)
    output_ds = None

    # Check the results
    output_ds = gdal.OpenEx(output_path, nOpenFlags=gdal.OF_VECTOR)
    output_layer = output_ds.GetLayer()
    layer_defn = output_layer.GetLayerDefn()

    output = f'{layer_defn.GetFieldDefn(0).GetName()} type: {layer_defn.GetFieldDefn(0).GetTypeName()}'
    for idx, feature in enumerate(output_layer):
        output += f"minx ({idx}): {feature.GetField('minx')}; "

    raise AssertionError(output)
