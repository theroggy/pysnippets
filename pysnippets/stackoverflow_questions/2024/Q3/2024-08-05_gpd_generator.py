import geopandas as gpd


def generator(gpkg_file, chunk_size, offset, layer_name):
    while True:
        query = f"""
        SELECT *
        FROM {layer_name}
        LIMIT {chunk_size} OFFSET {offset}
        """
        gdf = gpd.read_file(gpkg_file, sql=query)
        if gdf.empty:
            break
        yield gdf
        offset += chunk_size


path = "H:/Temp/OrlandoMSA2/OrlandoMSA2.gpkg"
for chunk in generator(path, 10, 0, "OrlandoMSA2"):
    print(len(chunk))

gpd.show_versions()
