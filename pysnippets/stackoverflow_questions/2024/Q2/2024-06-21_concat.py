import geopandas as gpd
import pandas as pd
import shapely

gdf1 = gpd.GeoDataFrame(
    [{"name": "L-shape", "geometry": shapely.Point(0, 1)}], crs="epsg:31370"
)
gdf2 = gdf1
gdf = pd.concat([gdf1, gdf2])

# Print some information to show/validate the result
print(f"{type(gdf)=}")
# type(gdf)=<class 'geopandas.geodataframe.GeoDataFrame'>
print(f"{gdf.crs.to_epsg()=}")
# gdf.crs.to_epsg()=31370
print(gdf)
#       name             geometry
# 0  L-shape  POINT (0.000 1.000)
# 0  L-shape  POINT (0.000 1.000)
