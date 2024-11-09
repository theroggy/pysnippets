"""Test GeoJSON with Fiona."""

import fiona

import pyogrio

pyogrio.set_gdal_config_options({"OGR_GEOJSON_MAX_OBJ_SIZE": 0.00001})

with fiona.open(
    "https://gist.githubusercontent.com/wavded/1200773/raw/e122cf709898c09758aecfef349964a8d73a83f3/sample.json"
) as src:
    pass
