import geofileops as gfo


def test_gfo_read_file(tmp_path):
    uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main/tests/data/polygon-parcel.gpkg"

    gdf = gfo.read_file(uri)

    assert gdf is not None, "Failed to read the file"
    assert len(gdf) > 0, "The GeoDataFrame is empty"
