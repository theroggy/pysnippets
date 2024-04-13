import geofileops as gfo
import geopandas as gpd
import shapely.geometry
import numpy as np

if __name__ == "__main__":
    np.random.seed(42)

    r = np.random.rand
    p = 4

    polygons = [
        shapely.geometry.Polygon([[r(), r()], [r(), r()], [r(), r()], [r(), r()]])
        for _ in range(10**p)
    ]
    df = gpd.GeoSeries(polygons)

    df.to_file(f"example_{p}.gpkg")
    gfo.makevalid(input_path=f"example_{p}.gpkg", output_path=f"madevalid_{p}.gpkg")
