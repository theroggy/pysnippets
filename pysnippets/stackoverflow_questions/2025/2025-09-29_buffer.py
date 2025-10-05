import geopandas as gpd
import shapely


bounds = (-79.403895, 39.3028665, -79.3876355, 39.3174215)

polygon = shapely.geometry.box(*bounds)
gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[polygon])
gdf_utm = gdf.to_crs(gdf.estimate_utm_crs(datum_name='NAD 83'))
gdf_utm_buffered = gdf_utm.buffer(0.01)
gdf_utm_buffered_wgs84 = gdf_utm_buffered.to_crs(epsg=4326)

print(gdf)
print(gdf_utm_buffered_wgs84)
