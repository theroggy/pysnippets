# -*- coding: utf-8 -*-
"""
Script to get geo data from Oracle. 
"""

import logging
from pathlib import Path
from typing import Optional

import cx_Oracle  # https://oracle.github.io/python-cx_Oracle/ 
import geofileops as gfo
import geopandas as gpd
import pyproj
from shapely.wkb import loads as sh_load_wkb

logger = logging.getLogger(__name__)

def read_oracle(
        connectionstring: str,
        sql_stmt: str,
        dst_crs: Optional[pyproj.CRS] = None) -> gpd.GeoDataFrame:
    """ 
    Execute sql statement and return as GeoDataFrame.

    More info on the connection string can be found [here]
    (https://cx-oracle.readthedocs.io/en/latest/user_guide/connection_handling.html#connection-strings).
    
    The sql statement should be someting of this form:
        
    `SELECT SDO_UTIL.TO_WKBGEOMETRY(geom) AS geometry_wkb FROM geo_table`
    
    Args:
        connectionstring (str): Connections string to the database.
        sql_stmt (str): SQL statement to execute. The geometry column should 
            be named geometry_wkb and should contain a WKB. An SDO_GEOMETRY
            can be converted to WKB using SDO_UTIL.TO_WKBGEOMETRY(). 
        dst (Path): Destination file path
        dst_crs (pyproj.CRS, optional): CRS to set to the output file. 
            Defaults to None.
        force (bool, optional): Overwrite destination file if it exists 
            already. Defaults to False.

    Raises:
        ValueError: This exception is raised if no column named geometry_wkb
            is selected in the sql_stmt.
    """
    # Connect
    connection = cx_Oracle.connect(connectionstring)
    try:
        # Define output type handler to fetch LOBs, avoiding the second round trip 
        # to the database to read the LOB contents
        connection.outputtypehandler = _output_type_handler

        cur = connection.cursor()
        cur.prefetchrows = 10000
        cur.arraysize = 10000
        cur.execute(sql_stmt)
        
        columns = [row[0] for row in cur.description]
        if "GEOMETRY_WKB" not in columns:
            raise ValueError("sql_stmt must select a column called GEOMETRY_WKB! Use SDO_UTIL.TO_WKBGEOMETRY() to convert a SDO_GEOMETRY to wkb.")
        
        geodata_gdf = gpd.GeoDataFrame(cur.fetchall(), columns=columns)

    finally:
        # Close connection
        connection.close()

    # Convert WKB column to proper geometry column
    geodata_gdf["geometry"] = gpd.GeoSeries(geodata_gdf["GEOMETRY_WKB"].apply(lambda x: sh_load_wkb(x)))
    del geodata_gdf["GEOMETRY_WKB"]

    # Add crs
    if dst_crs is not None:
        geodata_gdf.crs = dst_crs 
    if geodata_gdf.crs is None:
        logger.info("Geofile written without crs! Use crs parameter to add a crs.")
    
    return geodata_gdf

def _output_type_handler(cursor, name, default_type, size, precision, scale):
    """
    Define output type handler to fetch LOBs, avoiding the second round trip to
    the database to read the LOB contents.
    """
    if default_type == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)

def to_geofile(
        connectionstring: str,
        sql_stmt: str,
        dst: Path,
        dst_crs: Optional[pyproj.CRS] = None,
        force: bool = False):
    """ 
    Execute sql statement and save in a geo file. 

    Args:
        connectionstring (str): Connections string to the oracle database.
        sql_stmt (str): SQL statement to execute. The geometry column should 
            be named geometry_wkb and should contain a WKB. An SDO_GEOMETRY
            can be converted to WKB using SDO_UTIL.TO_WKBGEOMETRY(). 
        dst (Path): Destination file path
        dst_crs (pyproj.CRS, optional): CRS to set to the output file. 
            Defaults to None.
        force (bool, optional): Overwrite destination file if it exists 
            already. Defaults to False.

    Raises:
        ValueError: This exception is raised if no column named geometry_wkb
            is selected in the sql_stmt.
    """
    # If dest file exists already, remove it if force is True
    if dst.exists():
        if force is True:
            gfo.remove(dst)
        else:
            logger.info(f"Output file exists already, so stop: {dst}")
            return

    # Get data
    geodata_gdf = read_oracle(connectionstring, sql_stmt, dst_crs)

    # Save
    gfo.to_file(geodata_gdf, dst)
