"""
https://stackoverflow.com/questions/78996541/python-shapely-selection-of-a-given-part-of-a-geopandas-geometries
"""

from matplotlib import pyplot as plt
import shapely
import geopandas as gpd

road_borders = gpd.GeoDataFrame(
    {
        "geometry": [
            shapely.LineString([(0, 1), (9, 1), (9, 10)]),
            shapely.LineString([(0, -1), (9, -1), (9, -3)]),
            shapely.LineString([(11, 10), (11, 1), (13, 1)]),
            shapely.LineString([(11, -4), (11, -1), (14, -1)]),
        ],
        "id": [0, 1, 2, 3]
    },
    crs=4326
)

max_road_width = 2

road_border_points_dict = {"geometry": [], "id": []}
for border in road_borders.itertuples():
    border_points = shapely.points(shapely.get_coordinates(border.geometry))
    road_border_points_dict["geometry"].extend(border_points)
    road_border_points_dict["id"].extend([border.id] * len(border_points))

road_border_points = gpd.GeoDataFrame(
    road_border_points_dict, crs=road_borders.crs
    )
print(road_border_points)

road_border_point_buffers = road_border_points.buffer(
    max_road_width, cap_style="square"
)

sjoin = road_border_point_buffers.sjoin(road_border_point_buffers)

print(sjoin)

road_border_point_buffers.plot()
road_border_points.plot()
road_borders.plot()
plt.show()
