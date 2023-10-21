import geopandas as gpd
import topojson

url = "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"
gdf = gpd.read_file(url, driver="GPKG")
topo = topojson.Topology(gdf, topoquantize=False)
print("Ready")
