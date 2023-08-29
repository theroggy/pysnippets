from pathlib import Path

import geopandas as gpd
from matplotlib import pyplot as plt
import shapely
import shapely.plotting

script_dir = Path(__file__).resolve().parent
data_gdf = gpd.read_file(script_dir / "intersection_all.shp.zip")
result = shapely.intersection_all(data_gdf.geometry)

data_gdf.plot(alpha=0.50)
shapely.plotting.plot_polygon(result, color="red", add_points=False)
plt.show()
