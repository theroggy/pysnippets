import time
import geopandas as gpd
import numpy as np
import shapely
from shapely import Polygon


# Load some polygons as test data
poly_path = r"C:\temp\prc2024.gpkg"
polygons_gdf = gpd.read_file(poly_path, engine="pyogrio", columns=[], rows=1000)
polygons = polygons_gdf.geometry.tolist()

# For the first half of the polygons, use the centroid as points
points = (polygons_gdf.loc[: len(polygons) / 2].geometry.centroid).tolist()
# For the first quarter of the polygons, add the representative_point as points as well,
# so we have multiple points for those polygons
points2 = polygons_gdf.loc[: len(polygons) / 2].geometry.representative_point().tolist()
points.extend(points2)

# Test the performance using spatial index
start = time.perf_counter()
polygons_tree = shapely.STRtree(polygons)
result = polygons_tree.query(points, predicate="intersects")
mask = np.zeros(len(polygons), dtype=bool)
mask[np.unique(result[1])] = True
retained_polygons_tree = polygons_tree.geometries[~mask]
elapsed = time.perf_counter() - start
print(f"Retained {len(retained_polygons_tree)} polygons with tree, took {elapsed:.6f}")

# Test the performance using a simple loop
start = time.perf_counter()
retained_polygons: list[Polygon] = []
for polygon in polygons:
    if not any(polygon.contains(point) for point in points):
        retained_polygons.append(polygon)
elapsed = time.perf_counter() - start
print(f"Retained {len(retained_polygons)} polygons with loop, took {elapsed:.6f}")

# Make sure the results are the same
assert all(retained_polygons_tree == retained_polygons)
