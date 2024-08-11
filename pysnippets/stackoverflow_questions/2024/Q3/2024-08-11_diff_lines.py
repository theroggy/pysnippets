import geopandas as gpd
from matplotlib import pyplot as plt
import pandas as pd
from shapely import box, LineString

# Prepare test data
# -----------------
# Read the bike lanes
bike_lanes = "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/cycling-network/resource/bbf642be-a166-499e-9181-5a5b5223b37b/download/cycling-network.geojson"
bike_lanes_gdf = gpd.read_file(bike_lanes)

# Artificial route: the direct path + all bike lanes intersecting the direct path
route_direct_gdf = gpd.GeoDataFrame(
    geometry=[LineString([[-79.3873, 43.65049], [-79.3641171, 43.6613642]])],
    crs=bike_lanes_gdf.crs,
)
route_lane_gdf = bike_lanes_gdf.sjoin(route_direct_gdf, how="inner")
route_gdf = pd.concat([route_direct_gdf, route_lane_gdf])

# Routes that don't intersect with a bike lane
# --------------------------------------------
# Filter bike lanes that can intersect with the route
roi_gdf = gpd.GeoDataFrame(
    geometry=[box(*route_direct_gdf.total_bounds)], crs=bike_lanes_gdf.crs
)
bike_lanes_roi_gdf = bike_lanes_gdf.sjoin(roi_gdf, how="inner")
# Buffer the bike lanes to have some margin if they aren't exactly the same as the route
# The data is in geographic coordinates, so a distance is problematic. However, as it
# doesn't need to be exact... use a rough approximation.
distance = 2 / 100_000
bike_lanes_roi_gdf.geometry = bike_lanes_roi_gdf.buffer(distance, cap_style="flat")
# Apply difference
route_no_lane_gdf = route_gdf.overlay(bike_lanes_roi_gdf, how="difference")

# Plot input and result
ax = bike_lanes_roi_gdf.plot(color="blue")
route_gdf.plot(ax=ax, color="red")
route_no_lane_gdf.plot(ax=ax, color="yellow", linestyle="dashed")
plt.show()
