from osgeo import gdal

gdal.UseExceptions()

for geometrytype in ["MULTILINESTRING", "LINESTRING", "MULTIPOINT", "POINT"]:
    options = gdal.VectorTranslateOptions(geometryType=geometrytype)
    ds_output = gdal.VectorTranslate(
        srcDS="/vsicurl/https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg",
        destNameOrDestDS=f"C:/temp/force_type_{geometrytype}.gpkg",
        options=options,
    )
