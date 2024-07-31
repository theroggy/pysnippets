import os
import geopandas as gpd
import pygeoops


def extract_centerline_from_shp():
    shp_file_path = r"C:\temp\pygeos_error\road_ceterline_buffer-10-842-387.shp"
    gdf = gpd.read_file(shp_file_path)
    # gdf = gdf.to_crs(epsg=3857)

    # Remove points that are really close to each other to avoid errors when calculating
    # voronois in pygeoops.centerline
    gdf.geometry = gdf.geometry.remove_repeated_points(tolerance=1e-6)

    centerline_gdf = gpd.GeoDataFrame(geometry=[], crs=gdf.crs)
    for index, row in gdf.iterrows():
        centerline = pygeoops.centerline(row["geometry"], 1, -4.6, -0.1)
        centerline_gdf.loc[index, "geometry"] = centerline

    base_path = r"C:\temp\pygeos_error"
    road_output_shp = os.path.join(base_path, "pygeoops_centerline.shp")
    # centerline_gdf = centerline_gdf.to_crs(epsg=4326)
    centerline_gdf.to_file(road_output_shp, driver="ESRI Shapefile")


if __name__ == "__main__":
    extract_centerline_from_shp()
