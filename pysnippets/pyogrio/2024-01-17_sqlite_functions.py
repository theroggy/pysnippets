import geopandas as gpd
import pyogrio
import shapely

gdf = gpd.GeoDataFrame(geometry=[shapely.box(0, 0, 10, 10)], crs="epsg:4326")
sql = "SELECT name from pragma_function_list"

gpkg_path = "c:/temp/geoms.gpkg"
gdf.to_file(gpkg_path)
functions_gpkg = set(pyogrio.read_dataframe(gpkg_path, sql=sql)["name"].tolist())
hasspatialindex_gpkg = pyogrio.read_dataframe(
    gpkg_path, sql="SELECT hasspatialindex('geoms', 'geom')"
)["HasSpatialIndex"][0]
print(f"hasspatialindex on gpkg: {hasspatialindex_gpkg}")

sqlite_path = "c:/temp/db.sqlite"
gdf.to_file(sqlite_path, driver="SQLite")
functions_sqlite = set(pyogrio.read_dataframe(sqlite_path, sql=sql)["name"].tolist())
try:
    hasspatialindex_sqlite = pyogrio.read_dataframe(
        sqlite_path, sql="SELECT hasspatialindex('db', 'GEOMETRY')"
    )
    print(f"hasspatialindex on sqlite: {hasspatialindex_sqlite}")
except Exception as ex:
    print(f"hasspatialindex on sqlite failed with {ex}")

print(f"Missing for gpkg: {functions_gpkg - functions_sqlite}")
print(f"Missing for sqlite: {functions_sqlite - functions_gpkg}")
