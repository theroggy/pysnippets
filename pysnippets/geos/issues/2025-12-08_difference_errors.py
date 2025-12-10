
from pathlib import Path

import geopandas as gpd
import shapely
from shapely.geometry import Point

"""
GEOS error: TopologyException: found non-noded intersection between LINESTRING (63521.4 195200, 63513.7 195197) and LINESTRING (63516.7 195198, 63521.4 195200) at 63521.399077503709 195200.47748065522
GEOS error: TopologyException: unable to assign free hole to a shell at 151909.68711657077 182551.55750478432
GEOS error: TopologyException: unable to assign free hole to a shell at 142051.4753337577 185396.42400275171
GEOS error: TopologyException: unable to assign free hole to a shell at 165534.48763798922 200385.43918111175
GEOS error: TopologyException: unable to assign free hole to a shell at 161732.63323536515 228117.76643228158
"""

error_locs = [
    Point(63521.4, 195200),
    Point(63521.399077503709, 195200.47748065522),
    Point(151909.68711657077, 182551.55750478432),
    Point(142051.4753337577, 185396.42400275171),
    Point(165534.48763798922, 200385.43918111175),
    Point(161732.63323536515, 228117.76643228158),
]

task_dir = Path("//dg3.be/alp/gistmp/dataverwerking/2025-11-13_union_full")
input_path = task_dir / "FEITELIJK_GEBRUIK_2024_v3_fix_diss_feitelijkgebruik3.gpkg"
for error_loc in error_locs:
    # print(f"Processing error location at {error_loc.wkt}")
    gdf = gpd.read_file(input_path, bbox=error_loc.buffer(500).bounds)
    for idx, row in gdf.iterrows():
        for idx2, row2 in gdf.iterrows():
            if idx == idx2:
                continue
            geom1 = row["geometry"]
            geom2 = row2["geometry"]
            try:
                res = geom1.difference(geom2)
                if res.is_empty:
                    # print(f"Geometry at index {idx} is fully covered by geometry at index {idx2}")
                    pass
            except Exception as ex:
                print(f"Error between {geom1} and {geom2}: {ex}")

# print(gdf)
