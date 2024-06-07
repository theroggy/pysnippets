import difflib
from pathlib import Path
import tempfile

import geopandas as gpd
import geopandas.testing
import shapely


tmp_path = Path(tempfile.gettempdir())
gdf1 = gpd.read_file(
    "https://raw.githubusercontent.com/Deltares/hydromt/v1.0.0-alpha1/tests/data/naturalearth_lowres.geojson"
)
new_path = tmp_path / "world.geojson"
gdf1.to_file(new_path, driver="GeoJSON")
gdf2 = gpd.read_file(new_path)

# Compare
# gpd.testing.assert_geodataframe_equal(gdf1, gdf2)
print(f"{(shapely.equals(gdf1.iloc[14].geometry, gdf2.iloc[14].geometry))=}")

# Compare wkts
wkt1 = shapely.to_wkt(gdf1.iloc[14].geometry, rounding_precision=99)
wkt2 = shapely.to_wkt(gdf2.iloc[14].geometry, rounding_precision=99)
print(f"{(wkt1==wkt2)=}")

# Check validity of the invalid row gdf1 with itself
print(f"{(shapely.equals(gdf1.iloc[14].geometry, gdf1.iloc[14].geometry))=}")

# First make them valid, then check equality of those
gdf1_14_valid = shapely.make_valid(gdf1.iloc[14].geometry)
gdf2_14_valid = shapely.make_valid(gdf2.iloc[14].geometry)
print(f"{(shapely.equals(gdf1_14_valid, gdf2_14_valid))=}")
