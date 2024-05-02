import geopandas as gpd

wkt1 = "POLYGON((0 5, 5 5, 5 0, 0 0, 0 5))"
wkt2 = "POLYGON((0 0, 0 5, 5 5, 5 0, 0 0))"
wkt3 = "POLYGON((0 0, 0 5, 4 5, 5 5, 5 0, 0 0))"
sql = f"""
    SELECT GeomFromText('{wkt1}') = GeomFromText('{wkt1}') AS same_operator
        ,ST_Equals(GeomFromText('{wkt1}'), GeomFromText('{wkt1}')) AS same_st_equals
        ,GeomFromText('{wkt1}') = GeomFromText('{wkt2}') AS pointorder_operator
        ,ST_Equals(GeomFromText('{wkt1}'), GeomFromText('{wkt2}')) AS pointorder_st_equals
        ,GeomFromText('{wkt1}') = GeomFromText('{wkt3}') AS extrapoint_operator
        ,ST_Equals(GeomFromText('{wkt1}'), GeomFromText('{wkt3}')) AS extrapoint_st_equals
"""  # noqa: E501
print(gpd.read_file(":memory:", sql=sql, engine="pyogrio").transpose())
