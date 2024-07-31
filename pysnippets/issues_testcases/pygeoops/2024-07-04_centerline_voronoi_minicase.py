import os
import geopandas as gpd
import pygeoops
import shapely


def extract_centerline_from_shp():
    shp_file_path = r"C:\temp\pygeos_error\road_ceterline_buffer-10-842-387.shp"
    gdf = gpd.read_file(shp_file_path)
    # gdf = gdf.to_crs(epsg=3857)

    centerline_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)

    # Split in tiles
    tiles = gpd.GeoDataFrame(
        geometry=pygeoops.create_grid(
            total_bounds=gdf.total_bounds, nb_columns=50, nb_rows=50
        ),
        crs=gdf.crs,
    )
    gdf = gdf.overlay(tiles)

    for index, row in gdf.iterrows():
        if index != 271:
            continue
        try:
            shapely.voronoi_polygons(row["geometry"], only_edges=True)
            # centerline = pygeoops.centerline(row["geometry"], 1, -4.6, -0.1)
            # centerline_gdf.loc[index, "geometry"] = centerline
        except Exception as e:
            print(f"Error on index {index}: {e}")
            base_path = r"C:\temp\pygeos_error"
            error_gdf = gpd.GeoDataFrame(geometry=[row["geometry"]], crs=gdf.crs)
            error_path = os.path.join(base_path, "pygeoops_error.gpkg")
            # error_gdf.to_file(error_path)

    base_path = r"C:\temp\pygeos_error"
    road_output_shp = os.path.join(base_path, "pygeoops_centerline.shp")
    # centerline_gdf = centerline_gdf.to_crs(epsg=4326)
    centerline_gdf.to_file(road_output_shp, driver="ESRI Shapefile")


if __name__ == "__main__":
    extract_centerline_from_shp()
