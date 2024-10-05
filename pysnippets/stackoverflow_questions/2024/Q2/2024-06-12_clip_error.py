"""
https://stackoverflow.com/questions/78611605/cannot-clip-a-geodataframe-that-was-clipped-before-from-a-different-shapefile
"""

import geopandas as gpd
import pandas as pd
from shapely import box

# reading big, raw data
file1_raw = gpd.GeoDataFrame(
    data={"DATE_IST": [1, 2]}, geometry=[box(0, 0, 10, 10), box(50, 0, 60, 10)]
)
# reading outer shp
ind_shp = gpd.GeoDataFrame(geometry=[box(0, 0, 55, 55)])

# clip with country's extent
file1_proc1 = gpd.clip(file1_raw, ind_shp)
file1_proc2 = file1_proc1  # .drop(["some unwanted columns"], axis=1)

# reading another big raw file
file2_raw = gpd.GeoDataFrame(
    data={"DATE_IST": [1, 2]}, geometry=[box(0, 20, 10, 30), box(50, 50, 60, 60)]
)
# clip with country's extent
file2_proc1 = gpd.clip(file2_raw, ind_shp)
file2_proc2 = file2_proc1  # .drop(["some unwanted columns"], axis=1)
# concat both files
file_proc2 = pd.concat([file1_proc2, file2_proc2])

# subset based on year
mask = (file_proc2["DATE_IST"] > 0)
file_proc2_2014 = file_proc2.loc[mask].reset_index(drop=True)

# reading states shapefile
ind_st = gpd.GeoDataFrame(
    data={"Name": ["John", "Doe"]}, geometry=[box(0, 0, 2, 2), box(2, 2, 4, 4)]
)

state_names = ind_st["Name"].to_list()
clipped_dfs_holder = []

# clipping all states
for i in range(len(state_names)):
    current_state = ind_st[ind_st["Name"] == state_names[i]]
    df_st = gpd.clip(file_proc2_2014, current_state)
    clipped_dfs_holder.append(df_st)
    print("Clip complete for: " + state_names[i])
    print(df_st)
