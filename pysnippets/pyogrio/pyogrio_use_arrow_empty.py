import pyogrio

url = "https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
for use_arrow in [True, False]:
    gdf = pyogrio.read_dataframe(url, use_arrow=use_arrow, columns=[], read_geometry=False)
    print(f"\nuse_arrow={use_arrow}, len(gdf): {len(gdf)}, gdf:\n{gdf}")
