from osgeo import gdal
import geopandas as gpd

gdal.UseExceptions()

src = "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"

# If the geom column is the result of a Spatialite function and this results to NULL for
# the first row returned, all geometries in the column will be NULL.
dst_function_path = "/vsimem/dst_function.gpkg"
for order_by in ["DESC", "ASC"]:
    # Order by ASC -> NULL values will be last, so that will have proper results
    sql = f"""
        SELECT geom FROM
            (SELECT ST_Buffer(geom, -10) AS geom FROM parcels)
        ORDER BY geom IS NULL {order_by}
    """
    options = gdal.VectorTranslateOptions(
        SQLStatement=sql, geometryType="MULTIPOLYGON", layerName="parcels"
    )
    ds_output = gdal.VectorTranslate(
        srcDS=src, destNameOrDestDS=dst_function_path, options=options
    )
    print(
        f"geom column is Spatialite function, with order by {order_by}:\n{gpd.read_file(dst_function_path)}\n"
    )

# If the geom column is a simple column being selected that contains NULL for
# the first row returned, no problem.
dst = "/vsimem/output.gpkg"
for order_by in ["DESC", "ASC"]:
    sql = f"""
        SELECT geom FROM parcels
        ORDER BY geom IS NULL {order_by}
    """
    options = gdal.VectorTranslateOptions(
        SQLStatement=sql,
        geometryType="MULTIPOLYGON",
    )
    ds_output = gdal.VectorTranslate(
        srcDS=dst_function_path, destNameOrDestDS=dst, options=options
    )
    print(
        f"geom column is simple column, with order by {order_by}:\n{gpd.read_file(dst)}\n"
    )

gdal.Unlink(dst)
gdal.Unlink(dst_function_path)
