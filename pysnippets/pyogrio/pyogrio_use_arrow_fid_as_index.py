import pyogrio

url = "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"
for use_arrow in [True, False]:
    gdf = pyogrio.read_dataframe(url, use_arrow=use_arrow, fid_as_index=True)
    print(f"\nuse_arrow={use_arrow}, gdf.index:\n{gdf.index}")
