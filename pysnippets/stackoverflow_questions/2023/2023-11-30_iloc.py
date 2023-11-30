import pandas as pd
import geopandas as gpd
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

BeFra = world.loc[world['name'].isin(['France', 'Belgium'])]
print(BeFra)
