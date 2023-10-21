"""
Based on stackoverflow answer here:
https://gis.stackexchange.com/questions/452715/difference-between-df-geometry-buffer-and-df-geometry-scale-in-plain-english#:~:text=When%20you%20buffer%20you%20get,a%20fixed%20distance%20from%20it.&text=My%20coordinate%20system%20have%20meters,shape%20is%20enlarged%20or%20smallen.
"""

import geopandas as gpd
import shapely
import matplotlib.pyplot as plt

geoms = [
    "Polygon ((716228 7200069, 716072 7198883, 717168 7198760, 716228 7200069))",
    "Polygon ((714718 7200461, 713185 7199633, 714617 7200136, 713868 7199342, 714875 7200270, 714718 7200461))",
    "LineString (713487 7197585, 713610 7198659, 713968 7197541, 714192 7198547)",
]
geoms = [shapely.wkt.loads(x) for x in geoms]

df = gpd.GeoDataFrame(geometry=geoms, crs=3006)
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(25, 15))

df.plot(ax=ax1, color="blue")
df.plot(ax=ax2, color="blue")

for distance in range(50, 250, 50):
    df.buffer(distance).plot(ax=ax1, alpha=0.2)

for scale in range(11, 15, 4):
    df.scale(xfact=scale / 10, yfact=scale / 10, origin="centroid").plot(
        ax=ax2, alpha=0.1, color="green"
    )

plt.show()
