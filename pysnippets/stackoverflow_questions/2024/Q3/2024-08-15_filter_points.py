from pathlib import Path
import geopandas as gpd


poly_path = Path(r"C:\temp\prc2023\prc2023.gpkg")

points_gdf = gpd.read_file(r"C:\temp\prc2023\prc2023.gpkg", rows=5, engine="pyogrio")
points_gdf.geometry = points_gdf.geometry.centroid
layername = poly_path.stem

point_selects = [
    f"SELECT ST_Point({x}, {y}) AS geom"
    for x, y in points_gdf.geometry.get_coordinates().values.tolist()
]
points_unionall = "\nUNION ALL ".join(point_selects)

sql = f"""
    SELECT *
        FROM "{layername}" polys
        JOIN "rtree_{layername}_geom" polys_tree ON polys.fid = polys_tree.id
        JOIN ({points_unionall}
        ) points
    WHERE ST_MinX(points.geom) <= polys_tree.maxx
        AND ST_MaxX(points.geom) >= polys_tree.minx
        AND ST_MinY(points.geom) <= polys_tree.maxy
        AND ST_MaxY(points.geom) >= polys_tree.miny
        AND ST_intersects(polys.geom, points.geom) = 1
"""
print(f"{sql}")
polygons_gdf = gpd.read_file(poly_path, sql=sql)

print(polygons_gdf)
