"""
https://gis.stackexchange.com/questions/480964/algorithm-for-point-to-polygon-distance-calculations-in-shapely/480996?noredirect=1#comment784879_480996
"""

import geopandas as gpd

from shapely import box, Point
import matplotlib.pyplot as plt

# Some test data
polys = gpd.GeoDataFrame(
    data={
        "poly_name": ["poly_left", "poly_right"],
        "geometry": [box(0, 0, 2, 2), box(4, 0, 6, 2)],
    }
)
points = gpd.GeoDataFrame(
    {
        "point_name": ["point1", "point2", "point3", "point4"],
        "geometry": [Point(3, 0), Point(3, 1), Point(-0.5, 1), Point(-1, 3)],
    },
)

max_distance = 1

# If you want to be really exact, you can make the buffer distance a bit large
# and do additional filtering based on the exact distance to compensate for
# buffer creating approximate circles rather than real circles.
buffer_distance = max_distance * 1
points_buffer = points.copy()
points_buffer["geometry"] = points_buffer.geometry.buffer(max_distance)

# Join the buffered points with the polygons. Typically this result is already
# fine. This uses an rtree under the hood, so is fast.
within_distance = points_buffer.sjoin(polys, predicate="intersects")

# If it really needs to be exact and/or you want to know the distances,
# calculate the distances and/or do additional filtering here.
within_distance_points = gpd.GeoSeries(
    within_distance[["point_name"]].join(points[["geometry"]]).geometry
)
within_distance_polys = gpd.GeoSeries(
    within_distance[["index_right"]].set_index("index_right").join(polys).geometry
)
within_distance["distance"] = within_distance_points.distance(
    within_distance_polys, align=False
)
within_distance = within_distance.loc[within_distance["distance"] <= max_distance]

# Print result
print(within_distance[["point_name", "poly_name", "distance"]])
#   point_name   poly_name  distance
# 0     point1  poly_right       1.0
# 1     point2   poly_left       1.0
# 1     point2  poly_right       1.0
# 2     point3   poly_left       0.5

# Plot input data
fig, ax = plt.subplots()
polys.plot(ax=ax, edgecolor="blue", facecolor="none")
points.plot(
    ax=ax,
    color="red",
    facecolor="none",
)
points_buffer.plot(ax=ax, edgecolor="red", facecolor="none")
plt.show()
