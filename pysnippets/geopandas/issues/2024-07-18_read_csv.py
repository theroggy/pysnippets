from pathlib import Path
import geopandas as gpd

csv_path = Path(__file__).resolve().with_suffix(".csv")
with open(csv_path, "w") as f:
    f.write("name,y,lon\n")
    f.write("a,2,3\n")
    f.write("b,4,5\n")

gdf = gpd.read_file(
    csv_path,
    x_possible_names="x,lon,longitude",
    y_possible_names="y,lat,latitude",
)

print(f"{type(gdf)=}")
# type(gdf)=<class 'geopandas.geodataframe.GeoDataFrame'>

print(f"{gdf=}")
# gdf=  name    y  lon     geometry
# 0    a  2.0  3.0  POINT (3 2)
# 1    b  4.0  5.0  POINT (5 4)
