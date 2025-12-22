"""Issue repro for GDAL warning when adding a TEXT column to a GeoPackage table.

See:
"""

from osgeo import gdal

gdal.UseExceptions()

# Prepare test data
gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
gpkg_path = f"/vsicurl/{gfo_uri}/tests/data/polygon-parcel.gpkg"

# Add a column with valid type
datasource = gdal.OpenEx(gpkg_path)
sql = "SELECT ST_Length(ST_GeomFromText('POINT (0 0)')) AS length from parcels LIMIT 1"
result = datasource.ExecuteSQL(sql)
print(f"Executing {sql=}: {result=}")
datasource.ReleaseResultSet(result)
datasource = None
