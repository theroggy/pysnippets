import tempfile
from pathlib import Path

from osgeo import gdal

gdal.UseExceptions()

# Prepare test data
gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
gpkg_path = f"/vsicurl/{gfo_uri}/tests/data/polygon-parcel.gpkg"
tmp_dir = Path(tempfile.gettempdir())
test_path = tmp_dir / "polygon-parcel.gpkg"
if test_path.exists():
    test_path.unlink()
ds = gdal.VectorTranslate(destNameOrDestDS=test_path, srcDS=gpkg_path)
ds = None

# Add a column with valid type
datasource = gdal.OpenEx(str(test_path), nOpenFlags=gdal.OF_UPDATE)
sql_stmt = 'ALTER TABLE "parcels" ADD COLUMN "TEST_TEXT" TEXT'
result = datasource.ExecuteSQL(sql_stmt)
print(f"Executing {sql_stmt=}: {result=}")

# Add a column with invalid type -> does not raise an error
sql_stmt = 'ALTER TABLE "parcels" ADD COLUMN "TEST_INVALID" INVALID_TYPE'
result = datasource.ExecuteSQL(sql_stmt)
print(f"Executing {sql_stmt=}: {result=}")

# Check if columns were added -> column TEST_INVALID is not present
datasource_layer = datasource.GetLayer(0)
layer_defn = datasource_layer.GetLayerDefn()
for name in ["TEST_TEXT", "TEST_INVALID"]:
    field_index = layer_defn.GetFieldIndex(name)
    print(f"Field index of {name=}: {field_index}")

# Add column with duplicate name -> raises an error
sql_stmt = 'ALTER TABLE "parcels" ADD COLUMN "TEST_TEXT" INVALID_TYPE'
try:
    result = datasource.ExecuteSQL(sql_stmt)
except RuntimeError as e:
    print(f"Expected error executing {sql_stmt=}: {e}")
