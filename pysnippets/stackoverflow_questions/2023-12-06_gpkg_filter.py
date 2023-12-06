from pathlib import Path
import time
import geopandas as gpd
import numpy as np
import shapely.geometry

np.random.seed(42)
base=gpd.GeoSeries(shapely.geometry.Point(0,0).buffer(1,resolution=3))

circle_counts = [2000, 200000]
for circle_count in circle_counts:
    circles = gpd.GeoSeries(
        [
            shapely.geometry.Point(e)
            for e in np.random.uniform(low=-10, high=10, size=[circle_count, 2])
        ]
    ).buffer(distance=0.1)

    Path("example.gpkg").unlink(missing_ok=True)
    base.to_file("example.gpkg", layer="base")
    circles.to_file("example.gpkg", layer="circles")

    start = time.perf_counter()
    base = gpd.read_file("example.gpkg", layer="base")
    circles_filtered = gpd.read_file("example.gpkg", layer="circles", mask=base)
    print(f"For {circle_count} circles, took {time.perf_counter() - start} seconds")
