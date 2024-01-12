import geopandas
from shapely.geometry import Point

series_z = geopandas.GeoSeries([Point(1, 1, 1), Point(2, 2, 2), Point(3, 3, 3)])
print(series_z)

series_xy = geopandas.GeoSeries(geopandas.points_from_xy(x=series_z.x, y=series_z.y))
print(series_xy)
