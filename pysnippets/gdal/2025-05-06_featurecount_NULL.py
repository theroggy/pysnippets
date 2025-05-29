import tempfile

from osgeo import gdal

gdal.UseExceptions()


gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
src_path = f"/vsicurl/{gfo_uri}/tests/data/polygon-parcel.gpkg"
empty_path = f"{tempfile.gettempdir()}/polygon_parcel_empty.gpkg"
print(f"{empty_path=}")

options = gdal.VectorTranslateOptions(
    SQLStatement="SELECT * FROM parcels WHERE fid IS NULL",
    layerName="parcels",
    datasetCreationOptions=["ADD_GPKG_OGR_CONTENTS=NO"],
)
file = gdal.VectorTranslate(destNameOrDestDS=empty_path, srcDS=src_path, options=options)
file = None

empty2_path = f"{tempfile.gettempdir()}/polygon_parcel_empty2.gpkg"
print(f"{empty2_path=}")
file = gdal.VectorTranslate(destNameOrDestDS=empty2_path, srcDS=empty_path)
file = None
