from datetime import datetime
import geopandas as gpd

input = r"C:\Temp\prc2023\prc2023.gpkg"

gdf = gpd.read_file(input, rows=30000)


def try_buffer(geometry, distance):
    try:
        return geometry.buffer(distance)
    except:
        return None


start_time = datetime.now()

# gdf.geometry = [try_buffer(g, 305) for g in gdf.geometry]
# gdf.geometry = gdf.geometry.buffer(305)
# gdf.geometry = gdf.geometry.apply(lambda g: try_buffer(g, 305))
gdf["geometry"] = gdf["geometry"].apply(lambda g: try_buffer(g, 305))

"""
# To stop the loop
max = len(gdf)

# Indices
start = 0
end = 1

print(start_time)
failed_index = []
while start <= max:
    # gdf_copy = gdf.copy()
    gdf_copy = gdf[start:end].copy()

    # Try to return buffer geometry
    try:
        buffer = gdf_copy.geometry.buffer(305)
        gdf.loc[start, ["geometry"]] = buffer

    # If buffer function fails, return None
    except:
        gdf.loc[start, ["geometry"]] = None
        failed_index.append(start)

    start += 1
    end += 1
"""

print(f"Took: {datetime.now()-start_time}")
