import geopandas as gpd

df = gpd.read_file(r"C:\Temp\polygon_parcel\polygon-parcel.gpkg", ignore_geometry=True)
gdf = gpd.GeoDataFrame(df)

gdf.to_file("/vsimem/memoryfile_pyogrio.gpkg", engine="pyogrio")
result_pyogrio_gdf = gpd.read_file("/vsimem/memoryfile_pyogrio.gpkg")

gdf.to_file("/vsimem/memoryfile_fiona.gpkg", engine="fiona")
result_fiona_gdf = gpd.read_file("/vsimem/memoryfile_fiona.gpkg")

gdf2 = gpd.GeoDataFrame({"data_column": [1, 2, 3]})
gdf2.to_file("/vsimem/memoryfile_pyogrio2.gpkg", engine="pyogrio")
result_pyogrio2_gdf = gpd.read_file("/vsimem/memoryfile_pyogrio2.gpkg")

print(result_pyogrio_gdf)
print(result_fiona_gdf)
print(result_pyogrio2_gdf)
