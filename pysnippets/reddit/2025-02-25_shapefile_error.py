"""
Post
https://www.reddit.com/r/gis/comments/1ixzzg3/reading_shapefile_causing_exit_code_1/
"""

import geopandas as gpd

print(gpd.read_file(r"C:\Temp\NationalRoads2013\NationalRoads2013.shp"))
