import geopandas as gpd
import shapely

path = "https://github.com/geofileops/geofileops/raw/refs/heads/main/tests/data/polygon-parcel.gpkg"
gdf = gpd.read_file(path)
gdf.geometry = shapely.extract_unique_points(gdf.geometry)
gdf_points = gdf.explode()
gdf_points.to_file("coord.gpkg")
