import geopandas as gpd

myfile = r"J:\Test_Shapefile.shp"
outfile = r"J:\Test_Out_Shapefile.shp"

myfile = r"C:\Temp\polygon_parcel\polygon-parcel.gpkg"
outfile = r"C:\Temp\polygon_parcel\polygon-parcel_edited.gpkg"

gdf = gpd.read_file(myfile)

# Update the values of column index 4 as is the sample code, but using the column names
# is probably cleaner.
gdf.loc[0, "LBLHFDTLT"] = "Green"
gdf.loc[1, "LBLHFDTLT"] = "Blue"
gdf.loc[2, "LBLHFDTLT"] = "Red"
gdf.loc[3, "LBLHFDTLT"] = "Yellow"

gdf.to_file(outfile)
