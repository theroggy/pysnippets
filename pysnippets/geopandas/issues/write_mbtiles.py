from pathlib import Path
import tempfile
import geopandas as gpd


tmp_path = Path("C:/Temp")
gdf1 = gpd.read_file(
    "https://raw.githubusercontent.com/Deltares/hydromt/v1.0.0-alpha1/tests/data/naturalearth_lowres.geojson"
)
new_path = tmp_path / "world.mbtiles"
gdf1.to_file(new_path, driver="MBTiles")
