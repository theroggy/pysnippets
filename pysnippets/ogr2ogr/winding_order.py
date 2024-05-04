import os
# os.system("ogr2ogr C:/Temp/FR-communes/communes.gpkg C:/Temp/FR-communes/communes.shp")

os.system("ogr2ogr --config OGR_ORGANIZE_POLYGONS SKIP C:/Temp/FR-communes/communes2.gpkg C:/Temp/FR-communes/communes.shp")
