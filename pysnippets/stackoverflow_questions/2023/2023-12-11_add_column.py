import geofileops as gfo

path = "C:/Temp/polygon-parcel_31370_XYZ.gpkg"
layer = gfo.get_only_layer(path)
gfo.execute_sql(path, sql_stmt=f'ALTER TABLE "{layer}" ADD COLUMN new_column INTEGER DEFAULT 1234')
gdf = gfo.read_file(path)
print(gdf["new_column"])
