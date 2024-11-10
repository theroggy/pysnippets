"""
https://stackoverflow.com/questions/79154874/combine-different-shapefile-feature-classes-based-on-their-names
"""

import geopandas as gpd
from shapely import box

# vec_data = gpd.read_file("map.shp")
vec_data = gpd.GeoDataFrame(
    data={"DESCR_ENG": [
        "Meadow (Half Sheed Tara 20%)",
        "Meadow (permanent meadow)",
        "Pasture (tare 20%)/S28-6 Wooded pastures",
        'Grain',
    ]},
    geometry=[box(0, 0, 5, 5), box(5, 0, 10, 5), box(10, 0, 15, 5), box(15, 0, 20, 5)],
    crs=31370,
)

# Add new "Classes" column based on DESCR_ENG column
vec_data["Classes"] = None
vec_data.loc[vec_data["DESCR_ENG"].str.startswith("Meadow"), "Classes"] = "Agriculture"
vec_data.loc[vec_data["DESCR_ENG"].str.startswith("Pasture"), "Classes"] = "Cultivated"

# Print result
print(vec_data.head())

# Save to file
# vec_data.to_file("map_extended.shp")
