# Load packages
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import Polygon, Point

# Suppose there are a list of lat and a list of lon and their resolutions
lat = [28.45, 28.55, 28.65, 28.75, 28.85]
lon = [76.85, 76.95, 77.05, 77.15, 77.25, 77.35]
res_lat = 0.1
res_lon = 0.1


# List all the combinations of the given lat and lon
# So we have a dataframe representing grid centres
def expand_grid(input_list_of_lat, input_list_of_lon):
    """
    List all combinations of the given list of latitudes and the given list of longitudes.
    """
    points = [(A, B) for A in input_list_of_lat for B in input_list_of_lon]
    points = np.array(points)
    points_lat = points[:, 0]
    points_lon = points[:, 1]
    coordinates_of_full_grid = pd.DataFrame({"lat": points_lat, "lon": points_lon})
    return coordinates_of_full_grid


test_grid_df = expand_grid(lat, lon)


# For each grid, create a "shapely.geometry.polygon.Polygon"
def get_grid_polygon(centre_lat, centre_lon, res_lat, res_lon):
    # Create a list of tuples (lon,lat) to store information of grid corners
    grid_corners = [
        Point(centre_lon - res_lon / 2, centre_lat - res_lat / 2),  # bottom-left
        Point(centre_lon + res_lon / 2, centre_lat - res_lat / 2),  # bottom-right
        Point(centre_lon + res_lon / 2, centre_lat + res_lat / 2),  # top-right
        Point(centre_lon - res_lon / 2, centre_lat + res_lat / 2),
    ]  # top-left
    # Convert the corners to a list of points covering the area
    point_list = [
        grid_corners[0],
        grid_corners[1],
        grid_corners[2],
        grid_corners[3],
        grid_corners[0],
    ]
    # Create the polygon based on the above list of points
    polygon = Polygon([[p.x, p.y] for p in point_list])
    return polygon


# Apply the above function to the sample data frame
test_grid_df["polygon"] = np.nan

for i in range(test_grid_df.shape[0]):
    test_grid_df["polygon"][i] = get_grid_polygon(
        centre_lat=test_grid_df["lat"][i],
        centre_lon=test_grid_df["lon"][i],
        res_lat=res_lat,
        res_lon=res_lon,
    )

# Check the output
# Then you will see that the precisions of coordinates within the polygons are a mess
# How to round them while keeping the dtype as "shapely.geometry.polygon.Polygon"?
print(test_grid_df)
print(type(test_grid_df["polygon"][0]))

test_grid_df.polygon = shapely.set_precision(test_grid_df.polygon, grid_size=0.001)
print(test_grid_df)
print(type(test_grid_df["polygon"][0]))

"""
        lat    lon                                            polygon
    0   28.45  76.85  POLYGON ((76.8 28.5, 76.9 28.5, 76.9 28.4, 76....
    1   28.45  76.95  POLYGON ((76.9 28.5, 77 28.5, 77 28.4, 76.9 28...
    2   28.45  77.05  POLYGON ((77 28.5, 77.1 28.5, 77.1 28.4, 77 28...
    3   28.45  77.15  POLYGON ((77.1 28.5, 77.2 28.5, 77.2 28.4, 77....
    4   28.45  77.25  POLYGON ((77.2 28.5, 77.3 28.5, 77.3 28.4, 77....
    5   28.45  77.35  POLYGON ((77.3 28.5, 77.4 28.5, 77.4 28.4, 77....
    6   28.55  76.85  POLYGON ((76.8 28.6, 76.9 28.6, 76.9 28.5, 76....
    7   28.55  76.95  POLYGON ((76.9 28.6, 77 28.6, 77 28.5, 76.9 28...
    8   28.55  77.05  POLYGON ((77 28.6, 77.1 28.6, 77.1 28.5, 77 28...
    9   28.55  77.15  POLYGON ((77.1 28.6, 77.2 28.6, 77.2 28.5, 77....
    10  28.55  77.25  POLYGON ((77.2 28.6, 77.3 28.6, 77.3 28.5, 77....
"""
