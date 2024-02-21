import geopandas as gpd
import shapely

polys = [
    shapely.box(xmin=xmin, ymin=ymin, xmax=xmin + 10, ymax=ymin + 10)
    for xmin in range(0, 100, 10)
    for ymin in range(0, 100, 10)
]
grid = gpd.GeoDataFrame(geometry=polys)

# Search for polygons that intersect with the point
print(grid.iloc[grid.sindex.query(shapely.Point(55, 55), predicate="intersects")])
