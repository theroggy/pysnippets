"""Read and write a shapefile using pyogrio leads to RuntimeWarnings."""

from pathlib import Path

import geodatasets
import geofileops as gfo
import geopandas as gpd
from geopandas.testing import assert_geodataframe_equal

script_dir = Path(__file__).parent.resolve()

path = geodatasets.get_path("nybb")

print(gfo.get_layerinfo(path))

print(f"Reading {path}")
gdf = gpd.read_file(path)
#gdf["Shape_Area"] = gdf["Shape_Area"].astype("float32")

# Write to shapefile again
for engine, use_arrow in [("fiona", None), ("pyogrio", False), ("pyogrio", True)]:
    print("----------------------------------------------------")
    print(f"Writing {path} using {engine=}, {use_arrow=}")
    print("----------------------------------------------------")
    output_path = script_dir / f"out_{engine}_{use_arrow}.shp"
    if use_arrow is not None:
        gdf.to_file(output_path, engine=engine, use_arrow=use_arrow)
    else:
        gdf.to_file(output_path, engine=engine)

    # Warnings written:
    # RuntimeWarning: Value 1623819823.8099999 of field Shape_Area of feature 0 not
    # successfully written. Possibly due to too larger number with respect to field width
    #  ogr_write(

    read = gpd.read_file(output_path)
    assert_geodataframe_equal(read, gdf)
