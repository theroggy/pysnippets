import geopandas as gpd
import pandas as pd

autobahn = "A7"
columns = ["ref", "length_m"]

df_total = pd.DataFrame(columns=columns)

gdf = gpd.read_file(f"https://fliessbaden.de/wp-content/uploads/A7.geojson")
gdf = gdf.to_crs("ESRI:102031")

gdf["length_m"] = gdf.geometry.length

total_m = gdf['length_m'].sum()
total_km = total_m / 1000
print(autobahn + ": " + str(round(total_km, 2)) + " km")
