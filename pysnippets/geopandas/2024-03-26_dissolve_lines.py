from geopandas import GeoDataFrame
import shapely
from shapely import LineString

gdf1 = GeoDataFrame([
	{"geometry": LineString([ (355041.15, 6688781.25, 0), (355040.9629213488, 6688781.437078651, 9.7) ])},
	{"geometry": LineString([ (355041.15, 6688781.25, 0), (354841.1500000001, 6688781.25, 0) ])}
], crs="epsg:2154")

gdf2 = gdf1.dissolve()
print(f"{gdf2.loc[0, 'geometry']=}")
# gdf2.loc[0, 'geometry']=<MULTILINESTRING Z ((355041.15 6688781.25 0, 355040.963 6688781.437 9.7), (3...>

merged = shapely.line_merge(gdf1.geometry)
print(f"{merged[0]=}")
# merged[0]=<LINESTRING Z (355041.15 6688781.25 0, 355040.963 6688781.437 9.7)>
