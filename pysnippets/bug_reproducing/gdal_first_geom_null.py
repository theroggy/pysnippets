from pathlib import Path

import geofileops as gfo
import geopandas as gpd
from shapely import Polygon

# Prepare test data
data = [
    {
        "descr": "polygon1",
        "geometry": Polygon([(0, 0), (0, 5), (5, 5), (5, 0), (0, 0)]),
    },
    {
        "descr": "polygon2",
        "geometry": Polygon([(0, 0), (0, 15), (15, 15), (15, 0), (0, 0)]),
    },
]
input_gdf = gpd.GeoDataFrame(data=data, crs=31370)  # type: ignore

tmp_path = Path("C:/temp")
input_path = tmp_path / f"test.gpkg"
gfo.to_file(input_gdf, input_path)
layer = gfo.get_only_layer(input_path)
distance = -5
sql_stmt = f"""
    SELECT ST_CollectionExtract(
               ST_Buffer({{geometrycolumn}}, {distance}, 5), 3
           ) AS geom
          {{columns_to_select_str}}
      FROM "{layer}" layer
"""

# If first row becomes NULL due to the function, all geometries become NULL.
result_path = tmp_path / f"test_select_null.gpkg"
gfo.select(
    input_path=input_path,
    output_path=result_path,
    sql_stmt=sql_stmt,
)
result_gdf = gfo.read_file(result_path)
print(result_gdf)

# When the rows are ordered so the first row is not NULL, result is OK.
result_path = tmp_path / f"test_select_null_ordered.gpkg"
sql_stmt = f"SELECT * FROM ({sql_stmt}) ORDER BY geom IS NULL"
gfo.select(
    input_path=input_path,
    output_path=result_path,
    sql_stmt=sql_stmt,
)
result_gdf = gfo.read_file(result_path)
print(result_gdf)
