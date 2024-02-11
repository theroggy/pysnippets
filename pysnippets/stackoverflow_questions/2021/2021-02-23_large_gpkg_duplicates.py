# https://stackoverflow.com/questions/66031593/slicing-a-large-file-removing-duplicates-and-merging-into-output-using-pandas

import geopandas as gpd

path = r"C:\Temp\lds-nz-building-outlines\nz-building-outlines.gpkg"
df = gpd.read_file(
    path, engine="pyogrio", sql="SELECT DISTINCT id FROM nz_building_outlines"
)
print(df)


"""
    import geopandas as gpd

    fname = "/Output.gpkg"
    only_ids = gpd.read_file(fname, engine="pyogrio", sql="SELECT DISTINCT id FROM output")
    only_ids.to_csv("output.csv")
"""
