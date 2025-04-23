import geopandas

# common column bame
common_col = 'FlowId'

# temporary column name
temp_col = 'TempId'

# channel drainage area GeoDataFrame
cda_gdf = geopandas.read_file(r'C:\Temp\bla\code_data\channel_drainage_area.shp')
print(f"{len(cda_gdf.loc[~cda_gdf.is_valid])=}")
cda_gdf.geometry = cda_gdf.geometry.make_valid()

# stream drainage area GeoDataFrame
sda_gdf = geopandas.read_file(r'C:\Temp\bla\code_data\stream_drainage_area.shp')
print(f"{len(sda_gdf.loc[~sda_gdf.is_valid])=}")
sda_gdf.geometry = sda_gdf.geometry.make_valid()
sda_gdf = sda_gdf.rename(
    columns={common_col: temp_col}
)

# relationship of channel drainage areas within subbasin drainage areas
rcs_gdf = geopandas.sjoin(
    left_df=cda_gdf, 
    right_df=sda_gdf, 
    predicate='covered_by', 
    how='left'
)

# missing value checks in the temporary column
null_channel_ids = rcs_gdf[rcs_gdf[temp_col].isna()][common_col].tolist()
print(null_channel_ids)
