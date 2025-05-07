import geopandas as gpd
gpd.options.io_engine = 'fiona'

from shapely.geometry import Polygon
gdf = gpd.GeoDataFrame({'geometry': [
    Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    Polygon(((0, 0), (1, 0), (1, 1), (0, 0)))
]})

outfile = 'c:/temp/trash.geojson'
import os
if os.path.exists(outfile):
    os.remove(outfile)

driver = 'GeoJSONSeq'
for i in range(2):
    gdf.to_file(outfile, driver=driver)
    print(os.path.getsize(outfile))
