from pathlib import Path
import geofileops as gfo
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.geometry
import numpy as np
import time
import geofileops as gfo


def benchmark():
    np.random.seed(42)

    elapsed_original = []
    elapsed_rtree_in = []
    elapsed_rtree_join = []
    elapsed_gfo = []

    ns = [8, 16, 24, 32, 40, 48, 56, 64]
    for n in ns:
        path = Path(f"united_{n}.gpkg")
        if not path.exists():
            p = gpd.GeoSeries(
                [
                    shapely.geometry.box(j, i, j + 1, i + 1)
                    for i in range(n)
                    for j in range(n)
                ]
            )

            q = gpd.GeoSeries(
                [
                    shapely.geometry.Point(e)
                    for e in np.random.uniform(low=0, high=n, size=[n * n * 10, 2])
                ]
            ).buffer(distance=0.1)

            p.to_file(path, layer="p", engine="pyogrio")
            q.to_file(path, layer="q", engine="pyogrio")

        t0 = time.time()
        sql = """
            SELECT ST_Difference(
                        p.geom,
                        (SELECT ST_UNION(geom)
                           FROM q
                          WHERE ST_Intersects(p.geom,geom)
                        )
                   ) AS geom
              FROM p;
        """
        _ = gpd.read_file(path, sql=sql, engine="pyogrio")
        elapsed_original.append(time.time() - t0)

        t0 = time.time()
        sql = """
            SELECT (SELECT IIF( ST_UNION(layer2.geom) IS NULL,
                                layer1.geom,
                                ST_Difference(layer1.geom, ST_UNION(layer2.geom))
                           )
                      FROM q layer2
                      JOIN rtree_q_geom layer2tree ON layer2.rowid = layer2tree.id
                     WHERE ST_MinX(layer1.geom) <= layer2tree.maxx
                       AND ST_MaxX(layer1.geom) >= layer2tree.minx
                       AND ST_MinY(layer1.geom) <= layer2tree.maxy
                       AND ST_MaxY(layer1.geom) >= layer2tree.miny
                       AND ST_INTERSECTS(layer1.geom, layer2.geom) = 1
                   ) AS geom 
            FROM p layer1
        """
        _ = gpd.read_file(path, sql=sql, engine="pyogrio")
        elapsed_rtree_join.append(time.time() - t0)

        t0 = time.time()
        sql = """
            SELECT (SELECT IIF( ST_UNION(q.geom) IS NULL,
                                p.geom,
                                ST_Difference(p.geom, ST_UNION(q.geom))
                              )
                      FROM q
                     WHERE ROWID IN(
                             SELECT id
                               FROM rtree_q_geom
                              WHERE minx <= MbrMaxX(p.geom)
                                AND maxx >= MbrMinX(p.geom)
                                AND miny <= MbrMaxY(p.geom)
                                AND maxy >= MbrMinY(p.geom)
                           )
                       AND ST_Intersects(p.geom, geom)
                   ) AS geom
            FROM p;
        """
        _ = gpd.read_file(path, sql=sql, engine="pyogrio")
        elapsed_rtree_in.append(time.time() - t0)

        t0 = time.time()
        # Note: use subdivide_coords=-1, otherwise an error is raised that both layers
        # are in one input file: https://github.com/geofileops/geofileops/issues/451
        result_path = "result_erase.gpkg"
        gfo.erase(
            input_path=path,
            erase_path=path,
            output_path=result_path,
            input_layer="p",
            erase_layer="q",
            subdivide_coords=-1,
            force=True,
        )
        elapsed_gfo.append(time.time() - t0)

    # Plots
    plot_timings(ns, elapsed_original, elapsed_rtree_join, [], [])
    plot_timings(ns, [], elapsed_rtree_join, elapsed_rtree_in, elapsed_gfo)


def plot_timings(
    ns, elapsed_original, elapsed_rtree_join, elapsed_rtree_in, elapsed_gfo
):
    # Print all passed results
    plt.figure(figsize=(8, 4))
    if len(elapsed_original) > 0:
        print(f"elapsed_original: {elapsed_original}")
        plt.scatter([e**2 for e in ns], elapsed_original, c="r")
        plt.plot([e**2 for e in ns], elapsed_original, c="r", label="original")
    if len(elapsed_rtree_join) > 0:
        print(f"elapsed_rtree_join: {elapsed_rtree_join}")
        plt.scatter([e**2 for e in ns], elapsed_rtree_join, c="g")
        plt.plot([e**2 for e in ns], elapsed_rtree_join, c="g", label="rtree, join")
    if len(elapsed_rtree_in) > 0:
        print(f"elapsed_rtree_in: {elapsed_rtree_in}")
        plt.scatter([e**2 for e in ns], elapsed_rtree_in, c="b")
        plt.plot([e**2 for e in ns], elapsed_rtree_in, c="b", label="rtree, in")
    if len(elapsed_gfo) > 0:
        print(f"elapsed_gfo: {elapsed_gfo}")
        plt.scatter([e**2 for e in ns], elapsed_gfo, c="m")
        plt.plot([e**2 for e in ns], elapsed_gfo, c="m", label="geofileops.erase")
    plt.xlabel("Number of geometries in p")
    plt.ylabel("execution time")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    benchmark()
