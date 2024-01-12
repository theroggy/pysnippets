import os
from osgeo import gdal
import geopandas as gpd
import matplotlib.pyplot as plt


def get_OSM():
    """Download/crop water/land OSM polys if desired crop isn't on disk"""
    path_dst = os.path.join(os.getcwd(), "water_polygons_SW.json")
    path_osm = f"/vsizip/vsicurl/https://osmdata.openstreetmap.de/download/water-polygons-split-4326.zip/water-polygons-split-4326/water_polygons.shp"
    W, E, S, N = [-180, 0, -180, 0]
    # vector translate = 'ogr2ogr', f"-spat {W} {S} {E} {N}", '-f GeoJSON', path_dst, path_osm
    if not os.path.exists(path_dst):
        print(f"Downloading and cropping OSM water polygons to SE")
        # gdal.VectorTranslate(path_dst, path_osm, spatFilter=[W, S, E, N], format="GeoJSON")
        gdal.VectorTranslate(path_dst, path_osm, format="GeoJSON")

    print(f"Loading OSM water polygons from: {path_dst}")
    os.environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "5"
    gdf_osm = gpd.read_file(path_dst, engine="pyogrio")
    return gdf_osm


if __name__ == "__main__":
    gdf_OSM = get_OSM()  # get a large df of polys
    axes = gdf_OSM.plot(color="blue", edgecolor="black", alpha=0.25)
    plt.show()
