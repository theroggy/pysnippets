import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from geodatasets import get_path

df = pd.DataFrame(
    {
        "City": ["Tbilisi", "Batumi", "Kutaisi", "Rustavi"],
        "Country": ["Georgia", "Georgia", "Georgia", "Georgia"],
        "Latitude": [41.7225, 41.6458, 42.2500, 41.5472],
        "Longitude": [44.7925, 41.6417, 42.7000, 45.0111],
    }
)
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326"
)

world = geopandas.read_file(get_path("naturalearth.land"))
# print(world.)
# We restrict to Georgia
ax = world.clip([40, 40, 50, 45.0]).plot(color="white", edgecolor="black")
# We can now plot our ``GeoDataFrame``.
gdf.plot(ax=ax, color="red")

plt.show()
