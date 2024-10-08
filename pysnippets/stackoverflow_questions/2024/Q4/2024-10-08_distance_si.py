from time import perf_counter

import geopandas as gpd
import numpy as np
import pandas as pd

from pyproj import CRS, Transformer
from shapely.geometry import Point
from shapely.ops import transform


def select_points_for_multiple_locations_vectorized(df, locations_df, radius_km):
    R = 6371  # Earth's radius in kilometers

    # Convert degrees to radians
    df_lat_rad = np.radians(df['latitude'].values)[:, np.newaxis]
    df_lon_rad = np.radians(df['longitude'].values)[:, np.newaxis]
    loc_lat_rad = np.radians(locations_df['lat'].values)
    loc_lon_rad = np.radians(locations_df['lon'].values)

    # Haversine formula (vectorized)
    dlat = df_lat_rad - loc_lat_rad
    dlon = df_lon_rad - loc_lon_rad
    a = np.sin(dlat/2)**2 + np.cos(df_lat_rad) * np.cos(loc_lat_rad) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distances = R * c

    # Create a mask for points within the radius
    mask = distances <= radius_km

    # Get indices of True values in the mask
    indices = np.where(mask)

    result = pd.concat([df.iloc[indices[0]].reset_index(drop=True), locations_df.iloc[indices[1]].reset_index(drop=True)], axis=1)

    return result

def random_lat_lon(n=1, lat_min=-10., lat_max=10., lon_min=-5., lon_max=5.):
    """
    this code produces an array with pairs lat, lon
    """
    lat = np.random.uniform(lat_min, lat_max, n)
    lon = np.random.uniform(lon_min, lon_max, n)

    return np.array(tuple(zip(lat, lon)))


def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = CRS.from_proj4(
        f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0")
    tfmr = Transformer.from_proj(aeqd_proj, aeqd_proj.geodetic_crs)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres
    return transform(tfmr.transform, buf)

df = pd.DataFrame(random_lat_lon(n=1_000_000), columns=['latitude', 'longitude'])
locations_df = pd.DataFrame(random_lat_lon(n=300), columns=['lat', 'lon'])

# Current implemantation
start = perf_counter()
result = select_points_for_multiple_locations_vectorized(df, locations_df, radius_km=2)
print(f"{len(result)=}")
print(f"Took {perf_counter() - start}")

# Implementation using a spatial index
start = perf_counter()
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
locations_buffer_gdf = gpd.GeoDataFrame(
    locations_df,
    geometry=locations_df.apply(lambda row : geodesic_point_buffer(row.lat, row.lon, 2), axis=1),
)
result = gdf.sjoin(locations_buffer_gdf)
print(f"{len(result)=}")
print(f"Took {perf_counter() - start}")
