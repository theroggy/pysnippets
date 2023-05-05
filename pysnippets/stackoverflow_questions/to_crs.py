import geopandas as gpd
from shapely.geometry import Polygon

# create two dummy polygons
poly1 = Polygon([(0,0), (1,0), (1,1), (0,1)])
poly2 = Polygon([(1,1), (2,1), (2,2), (1,2)])

# create a geopandas DataFrame with two rows
data = {'name': ['Polygon 1', 'Polygon 2'], 'geometry': [poly1, poly2]}
df = gpd.GeoDataFrame(data, crs='EPSG:4326')
df.to_crs('EPSG:32610', inplace=True)

print(df['geometry'][0].area)
