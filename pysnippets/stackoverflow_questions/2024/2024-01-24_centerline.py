import pygeoops
import geopandas as gpd

# Load the polygon representing the road contour as a GeoDataFrame
shapefile_path = 'contorno_alpha02_suavizado025_cc.shp'
gdf = gpd.read_file(shapefile_path)

# Calculate centerline of the polygons
gdf.geometry = pygeoops.centerline(gdf.geometry)

# Save centerlines in a new shapefile.
output_shapefile_path = 'centerlines_shapefile_025_CC.shp'  
gdf.to_file(output_shapefile_path)
