import geopandas as gpd

# i1 = "selected.txt"
# f1 = open(i1, "r")
# f1_select = f1.read()
path = "C:/Temp/prc2023/prc2023.gpkg"

for n in range(10000, 100000, 10000):
    refids = gpd.read_file(path, rows=slice(0, n))["REF_ID"].to_list()

    refids_str = ",".join([f"{refid}" for refid in refids])
    f1_select = f"""
        SELECT * FROM "Landbouwgebruikspercelen_2023_-_Voorlopig_extractie_26-06-2023" m
        WHERE REF_ID IN ({refids_str})
    """
    where = f"REF_ID IN ({refids_str})"
    # where = " OR ".join([f"REF_ID={refid}" for refid in refids])
    
    # gdf = gpd.read_file(path, sql=f1_select, engine="pyogrio")
    gdf = gpd.read_file(path, where=where)
    print(f"n: {n}, len(where): {len(where)}")
