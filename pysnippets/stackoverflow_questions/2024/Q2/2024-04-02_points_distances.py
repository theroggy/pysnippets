import logging
from pathlib import Path

import geopandas as gpd
import geofileops as gfo


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    dir = Path("C:/Temp/cities")
    csv = dir / "worldcities.csv"
    gpkg = dir / "worldcities.gpkg"
    if not gpkg.exists():
        df = gpd.read_file(csv, engine="pyogrio", encoding="UTF-8")
        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df.lng, df.lat, crs="EPSG:4326")
        )
        gfo.to_file(gdf, gpkg)

    distances = dir / "distances.gpkg"
    sql_stmt = """
        SELECT layer.city AS city1, layer2.city AS city2
              ,ST_Distance(layer.geom, layer2.geom) AS distance
          FROM "{input_layer}" layer
          CROSS JOIN "{input_layer}" layer2
          WHERE layer.fid < layer2.fid
            {batch_filter}
    """
    gfo.select(
        gpkg,
        output_path=distances,
        sql_stmt=sql_stmt,
        nb_parallel=-1,
        batchsize=100,
        force=True,
    )

    '''
    sql_stmt = """
        SELECT layer1.*, layer2.*, ST_Distance(layer1.geom, layer2.geom) AS distance
          FROM "{input1_layer}" layer1
          CROSS JOIN "{input2_layer}" layer2
          WHERE layer1.fid <> layer2.fid
            {batch_filter}
    """
    gfo.select_two_layers(
        input1_path=gpkg,
        input2_path=gpkg,
        output_path=distances,
        sql_stmt=sql_stmt,
        nb_parallel=1,
        force=True,
    )
    '''
