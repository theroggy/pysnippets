import logging
from pathlib import Path
from time import perf_counter

import geofileops as gfo
import geopandas as gpd
from geofileops.util import _geoops_sql

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bbox = (5, 53, 16, 64)

    # shp_path = r"X:\PerPersoon\PIEROG\Taken\2025\2025-04-22_perf_read_file\land-polygons-split-4326\land_polygons.shp"
    shp_path = r"C:\Temp\land-polygons-split-4326\land_polygons.shp"
    gpkg_path = shp_path.replace(".shp", ".gpkg")
    gfo.copy_layer(shp_path, gpkg_path)

    gpkg_subd_path = gpkg_path.replace(".gpkg", "_subd.gpkg")
    if not Path(gpkg_subd_path).exists():
        _geoops_sql._subdivide_layer(
            Path(gpkg_path), None, Path(gpkg_subd_path), subdivide_coords=1000, keep_fid=False
        )

    start = perf_counter()
    gdf = gpd.read_file(gpkg_path, use_arrow=True)
    print(f"Read time gpkg full: {perf_counter() - start:.2f} seconds")
    print(f"Number of features: {len(gdf)}")

    start = perf_counter()
    gdf = gpd.read_file(gpkg_path, bbox=bbox, use_arrow=True)
    print(f"Read time gpkg bbox: {perf_counter() - start:.2f} seconds")
    print(f"Number of features: {len(gdf)}")

    start = perf_counter()
    gdf = gpd.read_file(gpkg_subd_path, bbox=bbox, use_arrow=True)
    print(f"Read time gpkg bbox subd: {perf_counter() - start:.2f} seconds")
    print(f"Number of features: {len(gdf)}")
