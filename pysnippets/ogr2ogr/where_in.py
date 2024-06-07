"""
Stackoverflow question:
https://gis.stackexchange.com/questions/482083/ogr2ogr-how-do-i-filter-a-shp-based-on-multiple-attribute-values
"""

from pathlib import Path
import os

out_path = Path("out.geojson")
if out_path.exists():
    out_path.unlink()

cmd = """ogr2ogr -where "FID IN (2,3)" -dialect OGRSQL out.geojson "/vsizip//vsicurl/https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
"""
os.system(cmd)
