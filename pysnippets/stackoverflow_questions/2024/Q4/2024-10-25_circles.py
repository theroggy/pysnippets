"""
https://stackoverflow.com/questions/79126042/how-to-efficiently-remove-overlapping-circles-from-the-dataset/79127424#79127424
"""

from pathlib import Path
import geopandas as gpd
from matplotlib import pyplot as plt
from pyproj import CRS, Transformer
from shapely.geometry import Point
from shapely.ops import transform


def geodesic_point_buffer(lat, lon, distance):
    # Azimuthal equidistant projection
    aeqd_proj = CRS.from_proj4(
        f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0")
    tfmr = Transformer.from_proj(aeqd_proj, aeqd_proj.geodetic_crs)
    buf = Point(0, 0).buffer(distance)  # distance in metres
    return transform(tfmr.transform, buf)

# Read the csv file with data
csv_path = Path(__file__).resolve().with_suffix(".csv")
points_df = gpd.read_file(csv_path, autodetect_type=True)

# Convert the points to circles by buffering them
points_buffer_gdf = gpd.GeoDataFrame(
    points_df,
    geometry=points_df.apply(
        lambda row : geodesic_point_buffer(row.latitude, row.longitude, row.estimated_radius), axis=1
    ),
    crs=4326,
)

# Determine the intersecting city buffers (result includes self-intersections)
intersecting_gdf = points_buffer_gdf.sjoin(points_buffer_gdf)

# Get all city buffers that intersect a city with a larger population
intersecting_larger_population_df = intersecting_gdf.loc[
    intersecting_gdf.population_left < intersecting_gdf.population_right
]

# Remove the city buffers that intersect with a larger population city buffer
result_gdf = points_buffer_gdf[
    ~points_buffer_gdf.index.isin(intersecting_larger_population_df.index)
]

# Plot result
ax = points_buffer_gdf.boundary.plot(color="red")
result_gdf.boundary.plot(color="blue", ax=ax)
plt.show()
