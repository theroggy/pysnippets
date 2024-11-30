"""Test the speed of overlay with geofileops."""

import logging
import time
import warnings
from pathlib import Path

import geofileops as gfo

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    warnings.filterwarnings("ignore")

    start = time.time()

    building_cols = [
        "oid",
        "aktualit",
        "gebnutzbez",
        "funktion",
        "anzahlgs",
        "gmdschl",
        "lagebeztxt",
        # "geometry",
    ]
    parcels_cols = [
        "oid", "aktualit", "nutzart", "bez", "flstkennz", # "geometry"
    ]

    alkis_dir = Path("H:/temp/ALKIS")
    buildings_paths = list(alkis_dir.glob("./*/GebauedeBauwerk.shp"))
    parcels_paths = list(alkis_dir.glob("./*/NutzungFlurstueck.shp"))

    buildings_path = alkis_dir / "GebauedeBauwerk.gpkg"
    if not buildings_path.exists():
        for path in buildings_paths:
            gfo.copy_layer(src=path, dst=buildings_path, dst_layer=buildings_path.stem, append=True, create_spatial_index=False)
        gfo.create_spatial_index(buildings_path)

    parcels_path = alkis_dir / "NutzungFlurstueck.gpkg"
    if not parcels_path.exists():
        for path in parcels_paths:
            gfo.copy_layer(src=path, dst=parcels_path, dst_layer=parcels_path.stem, append=True, create_spatial_index=False)
        gfo.create_spatial_index(parcels_path)

    # buildings_gdf = buildings_gdf.drop_duplicates(subset="oid", keep="first")
    # parcels_gdf = parcels_gdf.drop_duplicates(subset="oid", keep="first")
    print(f"geofileops: Prepare data duration: {(time.time() - start):.0f} s.")

    start_intersection = time.time()
    buildings_with_parcels_path = alkis_dir / "buildings_with_parcels.gpkg"
    gfo.intersection(buildings_path, parcels_path, buildings_with_parcels_path, input1_columns=building_cols, input2_columns=parcels_cols)
    print(f"geofileops: Load, intersection, save takes: {(time.time() - start_intersection):.0f} s.")

    print(f"geofileops: Total duration: {(time.time() - start):.0f} s.")
