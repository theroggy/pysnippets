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
fig, ax = plt.subplots(ncols=2, figsize=(15, 15))

for distance in range(50, 250, 50):
    df.buffer(distance).plot(ax=ax, alpha=0.2)

for scale in range(11, 15, 1):
    df.scale(xfact=scale / 10, yfact=scale / 10).plot(ax=ax, alpha=0.1, color="green")

# df.plot(ax=ax, color="blue")

plt.show()
