from datetime import datetime
from pathlib import Path

import geofileops as gfo
import geopandas as gpd

gpkg_path = Path("C:/temp/lds-nz-building-outlines/nz-building-outlines.gpkg")
gpkg2_path = Path("C:/temp/lds-nz-building-outlines/nz-building-outlines2.gpkg")
gpkg2_path.unlink(missing_ok=True)

start = datetime.now()
gdf = gpd.read_file(gpkg_path, engine="pyogrio", use_arrow=True)
print(f"read_file took {datetime.now()-start}")

start = datetime.now()
gfo.to_file(gdf, gpkg2_path, create_spatial_index=False)
print(f"to_file without index took {datetime.now()-start}")
start = datetime.now()
gfo.create_spatial_index(gpkg2_path)
print(f"creating the index took {datetime.now()-start}")

gpkg2_path.unlink()

start = datetime.now()
gfo.to_file(gdf, gpkg2_path)
print(f"to_file with index took {datetime.now()-start}")
gpkg2_path.unlink(missing_ok=True)
