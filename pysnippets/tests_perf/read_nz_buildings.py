from datetime import datetime
from pathlib import Path

import geofileops as gfo
import geopandas as gpd

gpkg_path = Path("C:/temp/lds-nz-building-outlines/nz-building-outlines.gpkg")
shp_path = gpkg_path.with_suffix(".shp")

if not shp_path.exists():
    gfo.copy_layer(gpkg_path, shp_path)

start = datetime.now()
gpd.read_file(gpkg_path, engine="pyogrio", use_arrow=True)
print(f"read gpkg took {datetime.now()-start}")

start = datetime.now()
gpd.read_file(shp_path, engine="pyogrio", use_arrow=True)
print(f"read shp took {datetime.now()-start}")
