import pyogrio

url = "https://download.geofabrik.de/europe/germany/baden-wuerttemberg-latest.osm.pbf"
pgdf = pyogrio.read_dataframe(
    url, sql="SELECT * FROM multipolygons LIMIT 100", sql_dialect="SQLITE"
)
print(pgdf)
