import geopandas

def split_lines(
    line_file,
    lid_col,
    point_file
):

    line_gdf = geopandas.read_file(line_file)

    point_gdf = geopandas.read_file(point_file)

    points_grouped = point_gdf.groupby(lid_col)

    split_lines = []

    for index, row in line_gdf.iterrows():
        line = row.geometry
        line_id = row[lid_col]
        if line_id in points_grouped.groups:
            split_points = points_grouped.get_group(line_id).geometry
            # print(list(split_points))
            interpolate_points = [shapely.line_interpolate_point(line, line.project(point)) for point in split_points]
            # print(interpolate_points)
            check_line_intersects_points = [line.intersects(point) for point in interpolate_points]
            # print(check_line_intersects_points)
            check_line_contains_points = [line.contains(point) for point in interpolate_points]
            # print(check_line_contains_points)
            # multi_point = shapely.MultiPoint(interpolate_points)
            # multi_lines = shapely.ops.split(line, multi_point)
            # for segment in multi_lines.geoms:
            #     split_lines.append({"geometry": segment, fid_col: line_id})
        else:
            split_lines.append({'geometry': line, lid_col: line_id})

    split_gdf = geopandas.GeoDataFrame(split_lines, crs=line_gdf.crs)

    return split_gdf

output = split_lines(
    line_file=r"c:\temp\data_test\line.shp",
    lid_col='flwpath_id',
    point_file=r"c:\temp\data_test\point.shp"
)
