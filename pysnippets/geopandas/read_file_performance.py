import os
from pathlib import Path
from time import perf_counter

import geopandas as gpd
import geofileops as gfo
from osgeo import gdal

gdal.UseExceptions()

os.environ["OGR_SQLITE_CACHE"] = "100"  # 100 MB cache for SQLite
#del os.environ["OGR_SQLITE_CACHE"]

path = r"C:\Temp\lds-nz-building-outlines\nz-building-outlines.gpkg"
sorted_path = r"C:\Temp\lds-nz-building-outlines\nz-building-outlines_sorted.gpkg"

if not Path(sorted_path).exists():
    info = gfo.get_layerinfo(path)
    print(info.total_bounds)

    extent_wkt = "POLYGON((1100000 4790000, 1100000 6200000, 2090000 6200000, 2090000 4790000, 1100000 4790000))"
    SQLStatement = f"""
        SELECT *
        FROM nz_building_outlines
        ORDER BY HilbertCode(geom, ST_GeomFromText('{extent_wkt}'), 11)
        --ORDER BY MbrMinX(geom), MbrMinY(geom)
    """
    options = gdal.VectorTranslateOptions(
        SQLStatement=SQLStatement,
        SQLDialect="SQLite",
        layerName="nz_building_outlines_sorted",
    )
    gdal.VectorTranslate(sorted_path, path, options=options)

start = perf_counter()
bbox = (1_500_000, 5_000_000, 1_700_000, 5_200_000)
gdf = gpd.read_file(path, bbox=bbox, engine="pyogrio", use_arrow=True)
print(f"read took {perf_counter() - start:.2f} seconds")
print(gdf)
