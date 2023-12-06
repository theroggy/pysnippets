from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.geometry
import numpy as np
import time

np.random.seed(42)

elapsedList = []
ns = [8, 16, 24, 32, 40, 48, 56, 64]

for n in ns:
    p = gpd.GeoSeries(
        [shapely.geometry.box(j, i, j + 1, i + 1) for i in range(n) for j in range(n)]
    )

    q = gpd.GeoSeries(
        [
            shapely.geometry.Point(e)
            for e in np.random.uniform(low=0, high=n, size=[n * n * 10, 2])
        ]
    ).buffer(distance=0.1)

    Path("united.gpkg").unlink(missing_ok=True)
    p.to_file("united.gpkg", layer="p", engine="pyogrio")
    q.to_file("united.gpkg", layer="q", engine="pyogrio")

    t0 = time.time()
    sql = """
        SELECT ST_Difference(
                    layer1.geom,
                    (SELECT ST_UNION(layer2.geom) 
                       FROM q layer2
                       JOIN rtree_q_geom layer2tree ON layer2.rowid = layer2tree.id
                      WHERE layer1tree.minx <= layer2tree.maxx
                        AND layer1tree.maxx >= layer2tree.minx
                        AND layer1tree.miny <= layer2tree.maxy
                        AND layer1tree.maxy >= layer2tree.miny
                        AND ST_INTERSECTS(layer1.geom, layer2.geom) = 1
                    )
               ) AS geom 
         FROM p layer1
         JOIN rtree_p_geom layer1tree ON layer1.rowid = layer1tree.id
    """
    diff = gpd.read_file("united.gpkg", sql=sql, engine="pyogrio")
    elapsedList.append(time.time() - t0)
    # diff.to_file("diff.gpkg", engine="pyogrio")

print(elapsedList)

plt.figure(figsize=(8, 4))
plt.scatter([e**2 for e in ns], elapsedList)
plt.plot([e**2 for e in ns], elapsedList, c="r")
plt.xlabel("Number of geometries in p")
plt.ylabel("ogrinfo execution time")
plt.show()
