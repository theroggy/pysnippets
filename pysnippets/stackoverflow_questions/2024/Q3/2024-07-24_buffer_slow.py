from datetime import datetime
import geopandas as gpd
from pathlib import Path
import shapely

ndvi_gdf_path = Path(r"D:\mypath\ndvi_gdf.gpkg")
ndvi_gdf_path = Path(r"C:/Temp/ndvi_gdf_small.gpkg")
ndvi_gdf = gpd.read_file(ndvi_gdf_path, engine="pyogrio", use_arrow=True)
ndvi_gdf.plot(column="category")

non_green_areas = ndvi_gdf[ndvi_gdf.category == 0]
len(non_green_areas)

non_green_areas = ndvi_gdf[ndvi_gdf.category == 0]
len(non_green_areas)  # 79832

non_green_areas_reduced = non_green_areas[non_green_areas.area > 250]
non_green_areas_reduced  # 390 rows

non_green_areas_reduced.crs  # epsg:25832

non_green_areas_reduced["nb_coords_orig"] = shapely.get_num_coordinates(
    non_green_areas_reduced.geometry
)
"""
non_green_areas_reduced.geometry = non_green_areas_reduced.geometry.simplify(0.5)
non_green_areas_reduced["nb_coords_simpl"] = shapely.get_num_coordinates(
    non_green_areas_reduced.geometry
)
"""

print(non_green_areas_reduced)

for row in non_green_areas_reduced.itertuples():
    start = datetime.now()
    shapely.buffer(row.geometry, -1.25)  # did not complete while writing this...
    took = datetime.now() - start
    if took.total_seconds() > 1:
        print(f"{row.Index}, {shapely.get_num_coordinates(row.geometry)} took: {took}")
