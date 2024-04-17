import fiona
import geopandas as gpd

gdf = gpd.GeoDataFrame(gpd.read_file(gpd.datasets.get_path("nybb")))

# memfile_path = "/vsimem/memoryfile.gpkg"
memfile_path = "C:/temp/memoryfile.gdb"
gdf.iloc[[0, 1]].to_file(memfile_path, driver="OpenFileGDB", layer="test1", engine="pyogrio")
layers = fiona.listlayers(memfile_path, list_all_tables="YES")

print(layers)
