import geopandas as gpd
import shapely

gdf = gpd.GeoDataFrame(
    geometry=[
        shapely.Polygon(
            [[50.0, 50.0], [50.0, 50.1], [50.1, 50.1], [50.1, 50.0], [50.0, 50.0]]
        )
    ]
)
coordinates = shapely.get_coordinates(gdf.geometry[0])
points = [shapely.Point(coordinate[0], coordinate[1]) for coordinate in coordinates]
coords_gdf = gpd.GeoDataFrame(geometry=points)
print(coords_gdf)

"""
Result:
                        geometry
    0  POINT (50.00000 50.00000)
    1  POINT (50.00000 50.10000)
    2  POINT (50.10000 50.10000)
    3  POINT (50.10000 50.00000)
    4  POINT (50.00000 50.00000)
"""
