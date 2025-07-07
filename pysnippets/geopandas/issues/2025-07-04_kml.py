from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point

path = Path(__file__).resolve().with_suffix(".kml")

# build a dict of columns: 2 text, 1 int, 1 float, and the geometry
data = {
    "text_a":   ["foo",   "bar",   "baz"],
    "text_b":   ["lorem", "ipsum", "dolor"],
    "int_val":  [1,       2,       3],
    "float_val":[0.1,     0.2,     0.3],
    "geometry": [
        Point(-105.0, 40.0),
        Point(-110.0, 45.0),
        Point(-115.0, 50.0),
    ],
}

# create the GeoDataFrame (with WGS84 lon/lat)
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

path.unlink(missing_ok=True)
gdf.to_file(path, driver="kml")
with open(path) as ff:
    print(ff.read())
