import geopandas as gpd
import shapely.geometry
import numpy as np
import time

np.random.seed(42)

elapsedList = []
ns = [8,16,24,32,40,48,56,64]

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
    
    !del -f united.gpkg
    p.to_file("united.gpkg",layer="p")
    q.to_file("united.gpkg",layer="q")
    
    t0 = time.time()
    !ogrinfo -q -sql "SELECT ST_Difference(p.geom, (SELECT ST_UNION(geom) from q WHERE ST_INTERSECTS(p.geom,geom))) AS geom FROM p" united.gpkg > /dev/null
    elapsedList.append(time.time()-t0)
