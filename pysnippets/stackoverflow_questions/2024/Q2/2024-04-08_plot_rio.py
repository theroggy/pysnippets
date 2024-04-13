from matplotlib import pyplot as plt
import shapely
import shapely.geometry
import rasterio.features
import rasterio.plot

poly1 = shapely.geometry.Polygon([(2, 2), (6, 2), (6, 6), (2, 6)])
poly2 = shapely.geometry.Polygon([(4, 4), (8, 4), (8, 8), (4, 8)])
rasterio.features.rasterize([poly1, poly2], out_shape=(10, 10), all_touched=True)
bldgs = rasterio.features.rasterize(
    [poly1, poly2], out_shape=(10, 10), all_touched=True
)

fig, ax = plt.subplots()
rasterio.plot.show(bldgs, ax=ax)
plt.savefig("test.png")
