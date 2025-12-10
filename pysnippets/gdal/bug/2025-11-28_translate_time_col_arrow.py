
import tempfile
from pathlib import Path

from osgeo import gdal

gdal.UseExceptions()

# Prepare test data
time_geojson = """{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [0, 0]
            },
            "properties": {
                "int_col": 1,
                "time_col": "12:00:00"
            }
        }
    ]
}"""

tmp_dir = Path(tempfile.gettempdir())
print(f"Using temporary directory: {tmp_dir}")
input_path = tmp_dir / "time_test.geojson"
with open(input_path, "w") as f:
    f.write(time_geojson)

# List the fields in the input file
ds = gdal.OpenEx(input_path, gdal.OF_VECTOR | gdal.OF_READONLY)
layer = ds.GetLayer()
layer_defn = layer.GetLayerDefn()
print(f"Number of fields in input geojson: {layer_defn.GetFieldCount()}")
for i in range(layer_defn.GetFieldCount()):
    field_defn = layer_defn.GetFieldDefn(i)
    print(f"Field {i}: {field_defn.GetNameRef()} ({field_defn.GetTypeName()})")
ds = None

for use_arrow in [False, True]:
    output_path = tmp_dir / f"time_test_arrow-{use_arrow}.geojson"

    if output_path.exists():
        output_path.unlink()

    arrow_api_key = "OGR2OGR_USE_ARROW_API"
    gdal.SetConfigOption(arrow_api_key, "YES" if use_arrow else "NO")

    print(f"--- {arrow_api_key}={gdal.GetConfigOption(arrow_api_key)} ---")

    # Copy the file
    options = gdal.VectorTranslateOptions()
    ds = gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path, options=options)
    ds = None

    # List the fields in the output file
    ds = gdal.OpenEx(output_path, gdal.OF_VECTOR | gdal.OF_READONLY)
    layer = ds.GetLayer()
    layer_defn = layer.GetLayerDefn()
    print(f"Number of fields in output gpkg: {layer_defn.GetFieldCount()}")
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i)
        print(f"Field {i}: {field_defn.GetNameRef()} ({field_defn.GetTypeName()})")
    for feature in layer:
        print("Feature:")
        for i in range(layer_defn.GetFieldCount()):
            field_defn = layer_defn.GetFieldDefn(i)
            field_name = field_defn.GetNameRef()
            field_value = feature.GetField(field_name)
            print(f"  {field_name}: {field_value}")
    ds = None
