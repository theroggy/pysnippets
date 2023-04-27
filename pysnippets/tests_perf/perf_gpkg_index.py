import shutil
from pathlib import Path
import subprocess
import tempfile
from timeit import default_timer as timer

from geofileops.util import _sqlite_util as sqlite_util
import geopandas as gpd
from osgeo import gdal
import shapely


def prepare_test_gdf() -> gpd.GeoDataFrame:
    # Prepare test data
    x, y = (0, 0)
    rects = []
    size = 10
    while y <= 10000:
        while x <= 10000:
            rect = (x, y, x + size, y + size)
            rects.append(rect)
            x += size
        x = 0
        y += size

    geoms = [shapely.box(*rect) for rect in rects]
    gdf = gpd.GeoDataFrame(geoms, columns=["geometry"], crs=31370)  # type: ignore
    print(f"Test dataset with {len(gdf)} squares prepared")

    return gdf


# Init some variables
data_dir = Path(tempfile.gettempdir()) / "perf_gpkg_index"
force = False
orderby = ""
# orderby = "ORDER BY random()"
cache_size = None
# cache_size = -50000
print(f"orderby used: <{orderby}>")
print(f"cache_size used: <{cache_size}>")
gdf = None

# Prepare output dir
if force:
    shutil.rmtree(data_dir, ignore_errors=True)
data_dir.mkdir(exist_ok=True, parents=True)

# Create the shp test file without spatial index
path = data_dir / "test.shp"
if not path.exists():
    if gdf is None:
        gdf = prepare_test_gdf()
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
        gdf = prepare_test_gdf()
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio", driver="FlatGeobuf")
    print(f"write {path.name} without spatial index took {timer()-start}")

# Create fgb (flatgeobuf) test file with spatial index
path = data_dir / "test_si.fgb"
if not path.exists():
    if gdf is None:
        gdf = prepare_test_gdf()
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="YES", engine="pyogrio", driver="FlatGeobuf")
    print(f"write {path.name} with spatial index took {timer()-start}")

# Create the gpkg test file with spatial index
path = data_dir / "test_with_si.gpkg"
if not path.exists():
    if gdf is None:
        gdf = prepare_test_gdf()
    start = timer()
    gdf.to_file(path, engine="pyogrio")
    print(f"write {path.name} with spatial index took {timer()-start}")

# Create the gpkg test file without spatial index
path = data_dir / "test_no_si.gpkg"
if not path.exists():
    if gdf is None:
        gdf = prepare_test_gdf()
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

# Create the gpkg test file without spatial index, add it afterwards
path = data_dir / "test_si_gdal.gpkg"
if not path.exists():
    if gdf is None:
        gdf = prepare_test_gdf()
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
        gdf = prepare_test_gdf()
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
        gdf = prepare_test_gdf()
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
    if gdf is None:
        gdf = prepare_test_gdf()
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

    # Create spatial index on the gpkg file, with default sqlite cache
    start = timer()
    sql_stmt = f"""
        CREATE TABLE "testje" AS
           SELECT "fid"
                 ,500 minx, 20000000 maxx
                 ,500 miny, 1000 maxy
            FROM "{path.stem}"
    """
    sql_stmt = f"""
        CREATE TABLE "testje" AS
           SELECT "fid"
                 ,ST_MinX("geom") minx, ST_MaxX("geom") maxx
                 ,ST_MinY("geom") miny, ST_MaxY("geom") maxy
            FROM "{path.stem}"
    """
    datasource = gdal.OpenEx(str(path), nOpenFlags=gdal.OF_UPDATE)
    result = datasource.ExecuteSQL(sql_stmt)
    datasource.ReleaseResultSet(result)
    print(f"in {path.name}: copy data to test table with gdal ST_MinX {timer()-start}")

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

# Create the gpkg test file without spatial index, then add one using only sqlite
path = data_dir / "test_gpkg-spatialite_rtree-sqlite.gpkg"
if not path.exists():
    if gdf is None:
        gdf = prepare_test_gdf()
    start = timer()
    gdf.to_file(path, SPATIAL_INDEX="NO", engine="pyogrio")
    print(f"write {path.name} without spatial index took {timer()-start}")

    # Create spatial index on the gpkg file, with default sqlite cache
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

# Create pure sqlite test file, then add one using only sqlite
path = data_dir / "testdb_via_python.sqlite"
# path.unlink(missing_ok=True)
if not path.exists():
    # Create spatial index on the gpkg file, with default sqlite cache
    start = timer()
    create_bboxes = """
        CREATE TABLE bboxes (
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          minx FLOAT,
          maxx FLOAT,
          miny FLOAT,
          maxy FLOAT
        );
    """
    insert_bboxes = """
        INSERT INTO bboxes(minx, maxx, miny, maxy)
          WITH RECURSIVE
            cnt(x) AS (
               SELECT 0
               UNION ALL
               SELECT x+10 FROM cnt
                LIMIT 1000
            )
          SELECT minx, maxx, miny, maxy
            FROM (SELECT x AS minx, x+10 AS maxx FROM cnt) x,
                 (SELECT x AS miny, x+10 AS maxy FROM cnt) y;
    """
    sqlite_util.execute_sql(path, [create_bboxes, insert_bboxes], use_spatialite=False)
    print(f"create test data in {path.name} took {timer()-start}")

    # Create rtree index on test table
    start = timer()
    create_rtree = """
        CREATE VIRTUAL TABLE bboxes_rtree
          USING rtree(id, minx, maxx, miny, maxy);
    """
    sqlite_util.execute_sql(path, create_rtree, use_spatialite=False)
    print(f"create test table rtree index in {path.name} took {timer()-start}")

    # Now fill it
    start = timer()
    pragma_cachesize = "PRAGMA cache_size=-128000;"
    fill_rtree = f"""
        INSERT INTO bboxes_rtree
          SELECT id, minx, maxx, miny, maxy
            FROM bboxes
           {orderby};
    """
    sqlite_util.execute_sql(path, [pragma_cachesize, fill_rtree], use_spatialite=False)
    print(f"fill test table rtree index in {path.name} took {timer()-start}")

# Create pure sqlite test file, then add one using only sqlite via sqlite.exe
path = data_dir / "testdb_via_sqlite-exe.sqlite"
path.unlink(missing_ok=True)
if not path.exists():
    # Create spatial index on the gpkg file, with default sqlite cache
    start = timer()
    create_bboxes = """
        CREATE TABLE bboxes (
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          minx FLOAT,
          maxx FLOAT,
          miny FLOAT,
          maxy FLOAT
        );
    """
    insert_bboxes = f"""
        INSERT INTO bboxes(minx, maxx, miny, maxy)
          WITH RECURSIVE
            cnt(x) AS (
               SELECT 0
               UNION ALL
               SELECT x+10 FROM cnt
                LIMIT 1000
            )
          SELECT minx, maxx, miny, maxy
            FROM (SELECT x AS minx, x+10 AS maxx FROM cnt) x,
                 (SELECT x AS miny, x+10 AS maxy FROM cnt) y
                 ;
    """
    sqlite_util.execute_sql(path, [create_bboxes, insert_bboxes], use_spatialite=False)
    print(f"create test data in {path.name} took {timer()-start}")

    # Create + fill rtree index on test table
    start = timer()
    create_rtree = """
        CREATE VIRTUAL TABLE bboxes_rtree
          USING rtree(id, minx, maxx, miny, maxy);
    """
    sqlite_util.execute_sql(path, create_rtree, use_spatialite=False)
    print(f"create test table rtree index in {path.name} took {timer()-start}")

    start = timer()
    sql_stmt = ""
    if cache_size is not None:
        sql_stmt += "PRAGMA cache_size={cache_size};\n"
    sql_stmt += f"""
        INSERT INTO bboxes_rtree
          SELECT id, minx, maxx, miny, maxy
            FROM bboxes
           {orderby};
    """

    sqlite_path = r"C:\Tools\SQLite\v3.41.2\sqlite3.exe"
    sqlite_path = r"X:\GIS\_Tools\SQLiteStudio\v3.3.3_spatialite\sqlite3.exe"
    # sqlite_path = Path(os.environ["CONDA_PREFIX"]) / "Library/bin/sqlite3.exe"
    subprocess.call([sqlite_path, str(path), sql_stmt])
    print(f"fill test table rtree index in {path.name} took {timer()-start}")
