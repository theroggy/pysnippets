import tempfile

from osgeo import gdal

gdal.UseExceptions()


gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
src_path = f"/vsicurl/{gfo_uri}/tests/data/polygon-parcel.gpkg"
zip_path = f"{tempfile.gettempdir()}/parcels.shp.zip"

file = gdal.VectorTranslate(destNameOrDestDS=zip_path, srcDS=src_path)
file = None
zip_file = gdal.OpenEx(zip_path, gdal.OF_VECTOR)
zip_layer = zip_file.GetLayer(0)
print(zip_layer.GetName())
