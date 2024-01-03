import logging
from pathlib import Path

import geofileops as gfo
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Polygon


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    polygon_1 = np.array([[1, 6, 7.8, 7.8, 1, 1], [4, 4, 6, 11, 11, 4]]).T
    polygon_2 = np.array(
        [[6, 14, 14, 11, 8.2, 9, 6, 6], [0.5, 0.5, 12, 12, 10, 4.2, 3.5, 0.5]]
    ).T

    poly_1 = Polygon(polygon_1)
    poly_2 = Polygon(polygon_2)

    gdf = gpd.GeoDataFrame(geometry=[poly_1, poly_2])
    gdf.to_file("polygons.gpkg")
    gfo.dissolve_within_distance(
        Path("polygons.gpkg"), Path("polygons_diss.gpkg"), distance=5, gridsize=0.0
    )
    result_gdf = gfo.read_file("polygons_diss.gpkg")

    print(result_gdf.iloc[0].geometry)
    pd.concat([result_gdf, gdf]).plot(color=["red", "blue", "green"], alpha=0.2)
    plt.show()
