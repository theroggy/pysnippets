import shutil
from pathlib import Path
import tempfile
from timeit import default_timer as timer

import geofileops as gfo
from geofileops.util import _sqlite_util as sqlite_util
import geopandas as gpd
from osgeo import gdal


def prepare_testfile(src_path: Path, dst_path: Path):
    # Read input data
    gfo.copy(src_path, dst_path)
    gfo.remove_spatial_index(dst_path)
    gfo.rename_layer(dst_path, new_layer=dst_path.stem)


def read_test_gdf(path: Path) -> gpd.GeoDataFrame:
    # Read input data
    gdf = gpd.read_file(path, engine="pyogrio")
    assert isinstance(gdf, gpd.GeoDataFrame)
    print(f"Test dataset with {len(gdf)} rows ready")
    return gdf


# Init some variables
data_dir = Path(tempfile.gettempdir()) / "perf_gpkg_index_realdata"
force = False
orderby = ""
# orderby = "ORDER BY random()"
print(f"orderby used: <{orderby}>")
input_dir = Path(r"X:\Monitoring\OrthoSeg\trees\output_vector\BEFL-2022-ofw")
input_path = input_dir / "trees_18_419_BEFL-2022-ofw.gpkg"
gdf = None

# Prepare output dir
if force:
    shutil.rmtree(data_dir, ignore_errors=True)
data_dir.mkdir(exist_ok=True, parents=True)

# Create the shp test file without spatial index
path = data_dir / "test.shp"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

    # Create spatial index on the shp file
    start = timer()
    datasource = gdal.OpenEx(str(path), nOpenFlags=gdal.OF_UPDATE)
    result = datasource.ExecuteSQL('CREATE SPATIAL INDEX ON "test"')
    datasource.ReleaseResultSet(result)
    print(f"create spatial index on {path.name} took {timer()-start}")

# Create fgb (flatgeobuf) test file without spatial index
path = data_dir / "test.fgb"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio", driver="FlatGeobuf")
    print(f"write {path.name} without spatial index took {timer()-start}")

# Create fgb (flatgeobuf) test file with spatial index
path = data_dir / "test_si.fgb"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="YES", engine="pyogrio", driver="FlatGeobuf")
    print(f"write {path.name} with spatial index took {timer()-start}")

# Create the gpkg test file with spatial index
path = data_dir / "test_with_si.gpkg"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, engine="pyogrio")
    print(f"write {path.name} with spatial index took {timer()-start}")

# Create the gpkg test file without spatial index
path = data_dir / "test_no_si.gpkg"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

# Create the gpkg test file without spatial index, add it afterwards
path = data_dir / "test_si_gdal.gpkg"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

    # Create spatial index on the gpkg file, using gdal function
    start = timer()
    datasource = gdal.OpenEx(str(path), nOpenFlags=gdal.OF_UPDATE)
    result = datasource.ExecuteSQL(f"SELECT CreateSpatialIndex('{path.stem}', 'geom')")
    datasource.ReleaseResultSet(result)
    print(f"create + fill spatial index on {path.name} with gdal took {timer()-start}")

# Create the gpkg test file without spatial index, but to add one with spatialite
path = data_dir / "test_si_spatialite.gpkg"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

    # Create spatial index on the gpkg file, with default sqlite cache
    start = timer()
    create_extensions = """
        CREATE TABLE gpkg_extensions
        (
            table_name TEXT,
            column_name TEXT,
            extension_name TEXT NOT NULL,
            definition TEXT NOT NULL,
            scope TEXT NOT NULL
        );
    """
    add_index = f"SELECT gpkgAddSpatialIndex('{path.stem}', 'geom');"
    sqlite_util.execute_sql(path, [create_extensions, add_index])
    print(f"create spatial index on {path.name} took {timer()-start}")

    # Now fill index
    start = timer()
    fill_index = f"""
        INSERT INTO "rtree_{path.stem}_geom"
           SELECT "fid"
                 ,ST_MinX("geom"), ST_MaxX("geom"), ST_MinY("geom"), ST_MaxY("geom")
            FROM "{path.stem}"
            {orderby}
    """
    sqlite_util.execute_sql(path, fill_index)
    print(
        f"fill spatial index using spatialite ST_MinX on {path.name} "
        f"took {timer()-start}"
    )

# Create the gpkg test file without spatial index, add one with spatialite, fill it
# with gdal
path = data_dir / "test_si_spatialite_fill-gdal.gpkg"
if not path.exists():
    if gdf is None:
        gdf = read_test_gdf(input_path)
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

    # Create spatial index on the gpkg file
    start = timer()
    create_extensions = """
        CREATE TABLE gpkg_extensions
        (
            table_name TEXT,
            column_name TEXT,
            extension_name TEXT NOT NULL,
            definition TEXT NOT NULL,
            scope TEXT NOT NULL
        );
    """
    add_index = f"SELECT gpkgAddSpatialIndex('{path.stem}', 'geom');"

    datasource = gdal.OpenEx(str(path), nOpenFlags=gdal.OF_UPDATE)
    result = datasource.ExecuteSQL(create_extensions)
    datasource.ReleaseResultSet(result)
    result = datasource.ExecuteSQL(add_index)
    datasource.ReleaseResultSet(result)

    # sqlite_util.execute_sql(path, [create_extensions, add_index, fill_index])
    print(f"create spatial index on {path.name} took {timer()-start}")

    # Now fill index
    start = timer()
    fill_index = f"""
        INSERT INTO "rtree_{path.stem}_geom"
           SELECT "fid"
                 ,ST_MinX("geom"), ST_MaxX("geom"), ST_MinY("geom"), ST_MaxY("geom")
            FROM "{path.stem}"
            {orderby}
    """
    result = datasource.ExecuteSQL(fill_index)
    datasource.ReleaseResultSet(result)
    print(f"fill spatial index using gdal ST_MinX on {path.name} took {timer()-start}")

# Create the gpkg test file without spatial index, then add one using only sqlite
path = data_dir / "test_gpkg-gdal_rtree-sqlite.gpkg"
# path.unlink(missing_ok=True)
if not path.exists():
    prepare_testfile(src_path=input_path, dst_path=path)

    # Create spatial index on the gpkg file, with default sqlite cache
    start = timer()
    sql_stmt = f"""
        CREATE TABLE "testje" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, ST_MaxX("geom") maxx
                 ,ST_MinY("geom") miny, ST_MaxY("geom") maxy
            FROM "{path.stem}"
            ORDER BY ST_MinX("geom"), ST_MinY("geom")
    """
    datasource = gdal.OpenEx(str(path), nOpenFlags=gdal.OF_UPDATE)
    result = datasource.ExecuteSQL(sql_stmt)
    datasource.ReleaseResultSet(result)
    datasource = None
    print(f"in {path.name}: copy data to test table with gdal ST_MinX {timer()-start}")

    # Create + fill rtree index on test table
    test_combinations = [
        (None, ""),
        (-5000000, ""),
        # (None, "ORDER BY random()"),
        # (-5000000, "ORDER BY random()"),
    ]

    for cur_cachesize, cur_orderby in test_combinations:
        start = timer()
        sql_stmts = []

        # Prepare rtree name based on params
        rtree_name = "rtree_testje"
        if cur_cachesize is not None:
            rtree_name = f"{rtree_name}_{cur_cachesize}"
            sql_stmts.append(f"PRAGMA cache_size={cur_cachesize}")
        if cur_orderby != "":
            rtree_name = f"{rtree_name}_orderby"

        # Prepare statements
        create_rtree = f"""
            CREATE VIRTUAL TABLE "{rtree_name}"
            USING rtree(id, minx, maxx, miny, maxy);
        """
        sql_stmts.append(create_rtree)
        fill_rtree = f"""
            INSERT INTO "{rtree_name}"
            SELECT fid, minx, maxx, miny, maxy
                FROM "testje"
                {cur_orderby}
        """
        sql_stmts.append(fill_rtree)
        sqlite_util.execute_sql(path, sql_stmts, use_spatialite=False)
        print(
            f"create + fill test rtree index {rtree_name} in {path.name} "
            f"took {timer()-start}"
        )

# Create the gpkg test file without spatial index, then add one using only sqlite
path = data_dir / "test_gpkg-spatialite_rtree-sqlite.gpkg"
# path.unlink(missing_ok=True)
if not path.exists():
    prepare_testfile(src_path=input_path, dst_path=path)

    # Create test table with bounding boxes
    start = timer()
    sql_stmt = f"""
        CREATE TABLE "testje" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, ST_MaxX("geom") maxx
                 ,ST_MinY("geom") miny, ST_MaxY("geom") maxy
            FROM "{path.stem}"
    """
    sqlite_util.execute_sql(path, sql_stmt)
    print(f"in {path.name}: copy to test table with spatialite ST_MinX {timer()-start}")

    # Create + fill rtree index on test table
    start = timer()
    create_rtree = """
        CREATE VIRTUAL TABLE rtree_testje
          USING rtree(id, minx, maxx, miny, maxy);
    """
    fill_rtree = f"""
        INSERT INTO "rtree_testje"
           SELECT fid, minx, maxx, miny, maxy
            FROM "testje"
            {orderby}
    """
    sqlite_util.execute_sql(path, [create_rtree, fill_rtree], use_spatialite=False)
    print(f"create + fill test table rtree index in {path.name} took {timer()-start}")

# Copy the bboxes from the gpkg table, but read different numbers of coordinates.
path = data_dir / "test_gpkg-gdal-testdata.gpkg"
# path.unlink(missing_ok=True)
if not path.exists():
    prepare_testfile(src_path=input_path, dst_path=path)

    # Create table with bboxes of gpkg file, just for warming up...
    sql_stmt = f"""
        CREATE TABLE "testje_heatup" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, 500000 maxx
                 ,100000 miny, 500000 maxy
            FROM "{path.stem}"
    """
    datasource = gdal.OpenEx(str(path), nOpenFlags=gdal.OF_UPDATE)
    result = datasource.ExecuteSQL(sql_stmt)
    datasource.ReleaseResultSet(result)

    # Create table with bboxes of gpkg file, but only minx
    start = timer()
    sql_stmt = f"""
        CREATE TABLE "testje_minx" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, 500000 maxx
                 ,100000 miny, 500000 maxy
            FROM "{path.stem}"
    """
    result = datasource.ExecuteSQL(sql_stmt)
    datasource.ReleaseResultSet(result)
    print(f"in {path.name}: to test table, gdal ST_MinX {timer()-start}")

    # Create table with bboxes of gpkg file, minx + maxx
    start = timer()
    sql_stmt = f"""
        CREATE TABLE "testje_minx_maxx" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, ST_MaxX("geom") maxx
                 ,100000 miny, 500000 maxy
            FROM "{path.stem}"
    """
    result = datasource.ExecuteSQL(sql_stmt)
    datasource.ReleaseResultSet(result)
    print(f"in {path.name}: to test table, gdal ST_MinX, ST_MaxX {timer()-start}")

    # Create table with bboxes of gpkg file, minx + maxx
    start = timer()
    sql_stmt = f"""
        CREATE TABLE "testje_minx_maxx_miny" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, ST_MaxX("geom") maxx
                 ,ST_MinY("geom") miny, 500000 maxy
            FROM "{path.stem}"
    """
    result = datasource.ExecuteSQL(sql_stmt)
    datasource.ReleaseResultSet(result)
    print(
        f"in {path.name}: to test table, gdal ST_MinX, ST_MaxX, ST_MinY {timer()-start}"
    )

    # Create table with complete bboxes of gpkg file
    start = timer()
    sql_stmt = f"""
        CREATE TABLE "testje_all" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, ST_MaxX("geom") maxx
                 ,ST_MinY("geom") miny, ST_MaxY("geom") maxy
            FROM "{path.stem}"
    """
    result = datasource.ExecuteSQL(sql_stmt)
    datasource.ReleaseResultSet(result)
    print(
        f"in {path.name}: to test table, gdal ST_MinX, ST_MaxX, ST_MinY, ST_MaxY "
        f"{timer()-start}"
    )
