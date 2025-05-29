import tempfile
from pathlib import Path

from osgeo import gdal

gdal.UseExceptions()


gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
src_path = f"/vsicurl/{gfo_uri}/tests/data/polygon-parcel.gpkg"
invalid_sql_path = Path(f"{tempfile.gettempdir()}/polygon_parcel_invalid_sql.gpkg")
print(f"{invalid_sql_path=}")

try:
    options = gdal.VectorTranslateOptions(
        SQLStatement="SELECT * FROM parcels WHERE unexisting_column IS NULL",
        layerName="parcels",
    )
    file = gdal.VectorTranslate(
        destNameOrDestDS=invalid_sql_path, srcDS=src_path, options=options
    )
    file = None
except RuntimeError as ex:
    print(ex)

print(f"{invalid_sql_path.exists()=}")

try:
    ds = gdal.OpenEx(invalid_sql_path, nOpenFlags=gdal.OF_VECTOR | gdal.OF_READONLY)
except RuntimeError as ex:
    print(f"Opening file read-only gives an error: {ex}")
finally:
    ds = None

ds = gdal.OpenEx(invalid_sql_path, nOpenFlags=gdal.OF_VECTOR | gdal.OF_UPDATE)
print("Opening file in update mode does not give an error...")
ds= None
