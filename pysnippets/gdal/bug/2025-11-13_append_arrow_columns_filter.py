import tempfile
from pathlib import Path

from osgeo import gdal

gdal.UseExceptions()

# Prepare test data
gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
orig_path = f"/vsicurl/{gfo_uri}/tests/data/polygon-parcel.gpkg"
tmp_dir = Path(tempfile.gettempdir())
no_fields_path = tmp_dir / "polygon-parcel.gpkg"

for use_arrow in [False, True]:
    for select_fields in [[], ["OIDN"]]:

        if no_fields_path.exists():
            no_fields_path.unlink()

        arrow_api_key = "OGR2OGR_USE_ARROW_API"
        gdal.SetConfigOption(arrow_api_key, "YES" if use_arrow else "NO")

        print(f"--- {arrow_api_key}={gdal.GetConfigOption(arrow_api_key)}, {select_fields=} ---")

        # Create a copy with no fields
        options = gdal.VectorTranslateOptions(selectFields=select_fields)
        ds = gdal.VectorTranslate(destNameOrDestDS=no_fields_path, srcDS=orig_path, options=options)
        ds = None

        # Check that the file actually has no fields
        ds = gdal.OpenEx(no_fields_path, gdal.OF_VECTOR | gdal.OF_READONLY)
        layer = ds.GetLayer()
        layer_defn = layer.GetLayerDefn()
        print(f"Number of fields in no-fields gpkg: {layer_defn.GetFieldCount()}")
        ds = None

        # Now append the original file again without fields
        options = gdal.VectorTranslateOptions(accessMode="append", selectFields=select_fields, addFields=True)
        ds = gdal.VectorTranslate(destNameOrDestDS=no_fields_path, srcDS=orig_path, options=options)
        ds = None

        # The file should still have no fields
        ds = gdal.OpenEx(no_fields_path, gdal.OF_VECTOR | gdal.OF_READONLY)
        layer = ds.GetLayer()
        layer_defn = layer.GetLayerDefn()
        print(f"Number of fields after appending original gpkg: {layer_defn.GetFieldCount()}")
        ds = None
