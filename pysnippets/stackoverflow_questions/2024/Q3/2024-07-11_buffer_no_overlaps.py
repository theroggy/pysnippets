# https://gis.stackexchange.com/questions/483678/buffer-without-overlaps-in-python

from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd

# load the csv file and convert to GeoDataFrame
points_path = Path(__file__).parent / "2024-07-11_buffer_no_overlaps_points_demo.csv"
df = pd.read_csv(points_path)
geometry = gpd.points_from_xy(df["Longitude"], df["Latitude"])
points = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# change to projected CRS
points = points.to_crs("EPSG:7856")

# create unique ID for points
points["point_id"] = np.arange(1, points.shape[0] + 1)

# create voronoi polygons
voronois = gpd.GeoDataFrame(geometry=points.voronoi_polygons(), crs=points.crs)
# The order of the voronoi polygons is not guaranteed, so sjoin the attributes of the
# points. Recover the index of the original points.
voronois = voronois.sjoin(points, predicate="intersects").set_index("index_right")
assert len(voronois) == len(points)

# specify buffer in meters
buffer = 10

# create a limit for voronois (union all points and buffer them)
limit = points.union_all().buffer(buffer)

# clip the voronois to the limit
result = voronois.clip(limit)
print(result)

# plot
ax = result.plot()
points.plot(ax=ax, color="red")
plt.show()
