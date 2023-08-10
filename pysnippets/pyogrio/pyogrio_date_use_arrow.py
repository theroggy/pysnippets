import pyogrio

url = "https://github.com/theroggy/pysnippets/raw/pysnippets/pyogrio/polygon-parcel_31370.zip"

for use_arrow in [True, False]:
    gdf = pyogrio.read_dataframe(url, use_arrow=use_arrow)
    print(
        f"use_arrow: {use_arrow}, column dtype: {gdf['DATUM'].dtype}, "
        f"value: {gdf['DATUM'][0]}, value type: {type(gdf['DATUM'][0])}"
    )
