import numpy as np
from shapely import polygons
import geopandas as gpd
from typing import Union
import geodatasets


def create_bounding_boxes(
    input_geometry: Union[gpd.GeoSeries, gpd.GeoDataFrame],
) -> gpd.GeoSeries:
    # Do your basic checks

    bounds = input_geometry.bounds

    # Use numpy to create the vertices of each respective bounding box
    bottom_left_vertex = np.array((bounds.minx.values, bounds.miny.values)).T.reshape(
        -1, 1, 2
    )
    bottom_right_vertex = np.array((bounds.maxx.values, bounds.miny.values)).T.reshape(
        -1, 1, 2
    )
    top_left_vertex = np.array((bounds.minx.values, bounds.maxy.values)).T.reshape(
        -1, 1, 2
    )
    top_right_vertex = np.array((bounds.maxx.values, bounds.maxy.values)).T.reshape(
        -1, 1, 2
    )

    bbox_vertices = np.concatenate(
        (bottom_left_vertex, bottom_right_vertex, top_right_vertex, top_left_vertex),
        axis=1,
    )

    return gpd.GeoSeries(
        data=polygons(bbox_vertices), index=input_geometry.index, crs=input_geometry.crs
    )


gdf = gpd.read_file(geodatasets.get_path("ny bb"))
bboxes = create_bounding_boxes(gdf)

print(bboxes)
print(gdf.envelope)
