import geopandas as gpd
import pandas as pd

autobahn = "A7"
columns = ["ref", "length_m"]
expected_distance = 1924
print(f"{autobahn}, expected distance: {expected_distance} km")

df_total = pd.DataFrame(columns=columns)

gdf = gpd.read_file(f"https://fliessbaden.de/wp-content/uploads/A7.geojson")

for crs in ["ESRI:102031", "EPSG:25833", "EPSG:32632", "EPSG:4839"]:
    gdf = gdf.to_crs(crs)

    gdf["length_m"] = gdf.geometry.length

    total_m = gdf['length_m'].sum()
    total_km = total_m / 1000
    print(f"{autobahn}, {crs} ({gdf.crs.name}): {str(round(total_km, 2))} km")
