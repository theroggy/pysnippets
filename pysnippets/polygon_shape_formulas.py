# Comparison of different formulas to judge a polygon's general shape

import math

import geopandas as gpd
import shapely.geometry as sh_geom


shapes = {}
shapes["square"] = {
    "geometry": sh_geom.Polygon([[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]]),
    "width_manual": 100,
    "length_manual": 100,
}
shapes["rectangle"] = {
    "geometry": sh_geom.Polygon([[0, 0], [200, 0], [200, 100], [0, 100], [0, 0]]),
    "width_manual": 100,
    "length_manual": 200,
}
shapes["rectangle_long"] = {
    "geometry": sh_geom.Polygon([[0, 0], [1000, 0], [1000, 100], [0, 100], [0, 0]]),
    "width_manual": 100,
    "length_manual": 1000,
}
shapes["circle"] = {
    "geometry": sh_geom.Point([0, 0]).buffer(100),
    "width_manual": 100,
    "length_manual": 100,
}

# Add calculated values
for shape in shapes:
    area = shapes[shape]["geometry"].area
    perimeter = shapes[shape]["geometry"].length

    shapes[shape]["width_indication_simple"] = round((2 * area) / perimeter, 2)
    shapes[shape]["width_indication_quadratic"] = round(
        (perimeter - math.sqrt(abs(perimeter**2 - 16 * area))) / 4, 2
    )
    shapes[shape]["perimeter"] = round(perimeter, 2)
    shapes[shape]["area"] = round(area, 2)
    # isoperimetric number
    shapes[shape]["roundness"] = round((4 * math.pi * area) / perimeter**2, 2)

shapes_gdf = gpd.GeoDataFrame(shapes)
print(shapes_gdf.query("index != 'geometry'"))
