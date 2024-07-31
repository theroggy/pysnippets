import shapely
import geopandas
import geopandas.testing

poly1 = shapely.Polygon([(0, 0), (0, 10), (10, 10), (5, 0), (0, 0)])
poly2 = shapely.Polygon([(5, 0), (8, 7), (10, 7), (10, 0), (5, 0)])

intersection_nogridsize = poly1.intersection(poly2)
gdf1 = geopandas.GeoDataFrame(geometry=[poly1, poly2])
gdf2 = geopandas.GeoDataFrame(geometry=[poly2, poly1])

geopandas.testing.assert_geodataframe_equal(gdf1, gdf2)
