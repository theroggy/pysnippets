"""
https://gis.stackexchange.com/questions/476187/how-to-drop-nearly-identical-point-locations-with-geopandas
"""

import pandas as pd
import geopandas as gpd
import shapely

df = pd.DataFrame(
    {
        "fid": [0, 1, 2, 3, 4, 5],
        "location_name": ["ABC", "ABC", "DEF", "DEF", "JKL", "JKL"],
        "equipment": ["tank", "tank", "generator", "generator", "tank", "generator"],
    }
)

coords = [
    "POINT (-68.85052703049803 -46.03444179295434)",
    "POINT (-68.85052703049802 -46.03443956295743)",
    "POINT (-68.60401999999993 -37.49876999999998)",
    "POINT (-69.17996992199994 -38.91214629699994)",
    "POINT (-69.29235725099994 -38.55542628499995)",
    "POINT (-69.29235725099992 -38.5554262849999)",
]

gdf = gpd.GeoDataFrame(data=df, geometry=gpd.GeoSeries.from_wkt(coords), crs=4326)

print(gdf)

# Round the coordinates to 5 decimals
gdf.geometry = shapely.set_precision(gdf.geometry, grid_size=0.00001)
print(gdf.drop_duplicates(["location_name", "equipment", "geometry"]))
