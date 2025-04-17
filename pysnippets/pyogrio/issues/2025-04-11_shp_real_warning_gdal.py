"""Read and write a shapefile using ogr2ogr leads to RuntimeWarnings."""

from pathlib import Path
from osgeo import gdal

gdal.UseExceptions()

data_dir = Path(__file__).parent.resolve() / "data"
data_dir.mkdir(exist_ok=True)

for real_value in ["1623819823.809", "1186924686.49", "3045212795.19", "3045212795.19", "636471539.774", "123456789.774", "12345678.774"]:
    print(f"\n## Write shapefile with {real_value=}, print as float/double with 20 decimals: {float(real_value):.20f}")
    json = """
    {
        "type": "FeatureCollection",
        "name": "precision",
        "features": [
                {
                    "type": "Feature",
                    "properties": { "area": __REAL_VALUE__ },
                    "geometry": { "type": "Point", "coordinates": [ 1.0, 1.0 ] }
                }
            ]
    }
    """

    json_path = data_dir / "precision.json"
    with open(json_path, "w") as f:
        f.write(json.replace("__REAL_VALUE__", real_value))

    shp_path = data_dir / "precision.shp"
    gdal.VectorTranslate(destNameOrDestDS=shp_path, srcDS=json_path)

    # Read shapefile and compare area with the original value
    dataSource = gdal.OpenEx(shp_path, 0)
    layer = dataSource.GetLayer()

    for feature in layer:
        print(f"Are values equal? {(feature.GetField('area') == float(real_value))=}")
    dataSource = None
