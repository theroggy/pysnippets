from osgeo import gdal
import geopandas as gpd

gdal.UseExceptions()

src = "/vsizip//vsicurl/https://github.com/geofileops/geofileops/raw/main/tests/data/poly_shp.zip"

# If the geom column is the result of a Spatialite function and this results to NULL for
# the first row returned, all geometries in the column will be NULL.
dst = "/vsimem/dst_function.gpkg"
for order_by in ["DESC", "ASC"]:
    # Order by ASC -> NULL values will be last, so that will have proper results
    sql = f"""
        SELECT geom FROM
            (SELECT ST_Buffer(geometry, -100) AS geom FROM "poly")
        ORDER BY geom IS NULL {order_by}
    """
    options = gdal.VectorTranslateOptions(
        SQLStatement=sql, SQLDialect="SQLite", geometryType="MULTIPOLYGON"
    )

    try:
        ds_output = gdal.VectorTranslate(
            srcDS=src, destNameOrDestDS=dst, options=options
        )
        print(
            f"geom column is Spatialite function, with order by {order_by}:\n{gpd.read_file(dst)}\n"
        )
    except Exception as e:
        print(
            f"geom column is Spatialite function, with order by {order_by}:\nError: {e}\n"
        )

gdal.Unlink(dst)
