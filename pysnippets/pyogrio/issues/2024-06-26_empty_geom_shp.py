import tempfile
from pyogrio.geopandas import read_dataframe, write_dataframe
import geopandas as gp
import shapely

for geom in [shapely.from_wkt("POINT EMPTY"), None]:
    for suffix in [".shp", ".gpkg"]:
        gdf = gp.GeoDataFrame({"x": [0]}, geometry=[geom], crs=4326)

        filename = f"{tempfile.gettempdir()}/test{suffix}"
        write_dataframe(gdf, filename)
        df = read_dataframe(filename)
        print(f"{suffix=}, {geom=}:  {df.geometry.iloc[0]}")
        # suffix='.shp', geom=<POINT EMPTY>:  None
        # suffix='.gpkg', geom=<POINT EMPTY>:  POINT EMPTY
        # suffix='.shp', geom=None:  None
        # suffix='.gpkg', geom=None:  None
