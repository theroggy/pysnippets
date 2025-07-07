import pyogrio

def test_pyogrio_read_dataframe(tmp_path):
    uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main/tests/data/polygon-parcel.gpkg"

    gdf = pyogrio.read_dataframe(uri)

    assert gdf is not None, "Failed to read the file"
    assert len(gdf) > 0, "The GeoDataFrame is empty"
