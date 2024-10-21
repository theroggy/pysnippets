from osgeo import gdal

gdal.UseExceptions()
options = gdal.VectorTranslateOptions(explodeCollections=True)
ds_output = gdal.VectorTranslate(
    srcDS="/vsicurl/https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg",
    destNameOrDestDS="C:/temp/empty_exploded.gpkg",
    options=options,
)
