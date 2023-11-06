from pathlib import Path
import tempfile

import geopandas as gpd
import pyogrio

tmp_dir = Path(tempfile.gettempdir())
url = "https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
for use_arrow in [True, False]:
    gdf = pyogrio.read_dataframe(url, use_arrow=use_arrow)
    print(
        f"input_file, use_arrow: {use_arrow}, column dtype: {gdf['DATUM'].dtype}, "
        f"value: {gdf['DATUM'][0]}, value type: {type(gdf['DATUM'][0])}"
    )
    written_path = tmp_dir / f"output_{use_arrow}.shp"
    pyogrio.write_dataframe(gdf, written_path)
    gdf = pyogrio.read_dataframe(written_path, use_arrow=False)
    print(
        f"written_file, use_arrow: {use_arrow}, column dtype: {gdf['DATUM'].dtype}, "
        f"value: {gdf['DATUM'][0]}, value type: {type(gdf['DATUM'][0])}"
    )

# Do a round-trip using fiona for comparison
gdf = gpd.read_file(url, engine="fiona")
print(
    f"input_file, fiona, column dtype: {gdf['DATUM'].dtype}, "
    f"value: {gdf['DATUM'][0]}, value type: {type(gdf['DATUM'][0])}"
)
written_path = tmp_dir / "output_fiona.shp"
gdf.to_file(written_path)
gdf = gpd.read_file(written_path, engine="fiona")
print(
    f"written_file, fiona, column dtype: {gdf['DATUM'].dtype}, "
    f"value: {gdf['DATUM'][0]}, value type: {type(gdf['DATUM'][0])}"
)
