import geopandas as gpd
import shapely
from shapely import Point

gpd.show_versions()

input = gpd.GeoDataFrame(
    {
        "userid": [1, 2, 2, 3, 3], 
        "geometry": [
            Point(0,0), Point(1,0), Point(1,1), Point(2,0), Point(2,1)
        ],
    },
    crs="EPSG:31370",
)

diss = input.dissolve(by="userid")
diss_multi = diss.loc[diss.geometry.type == "MultiPoint"]

print(diss)

lines = diss_multi.set_geometry(
    diss_multi.geometry.apply(lambda x: shapely.LineString(shapely.get_coordinates(x)))
)

print(lines)
