import geopandas
import shapely
import matplotlib.pyplot as plt


def split_lines(line_gdf, lid_col, point_gdf, tolerance):
    points_grouped = point_gdf.groupby(lid_col)

    split_lines = []
    lines_not_split = []
    for index, row in line_gdf.iterrows():
        line = row.geometry
        line_id = row[lid_col]
        if line_id in points_grouped.groups:
            split_points = points_grouped.get_group(line_id).geometry
            # print(list(split_points))
            #interpolate_points = [shapely.line_interpolate_point(line, line.project(point)) for point in split_points]
            # print(interpolate_points)
            #check_line_intersects_points = [line.intersects(point) for point in interpolate_points]
            # print(check_line_intersects_points)
            #check_line_contains_points = [line.contains(point) for point in interpolate_points]
            # print(check_line_contains_points)
            #multi_point = shapely.MultiPoint(interpolate_points)
            if len(split_points) == 1:
                split_point = split_points.item()
            else:
                split_point = shapely.MultiPoint(split_points.to_list())
            # line = shapely.ops.snap(line, split_point, tolerance)
            multi_lines = shapely.ops.split(line, split_point)
            if len(multi_lines.geoms) <= 1:
                lines_not_split.append({"geometry": line, lid_col: line_id, "split": "FAILED"})
            for segment in multi_lines.geoms:
                split_lines.append({"geometry": segment, lid_col: line_id, "split": "OK"})
        else:
            split_lines.append({'geometry': line, lid_col: line_id, "split": "NA"})

    split_gdf = geopandas.GeoDataFrame(split_lines, crs=line_gdf.crs)

    return split_gdf

line_gdf = geopandas.read_file(r"c:\temp\data_test\line.shp")
point_gdf = geopandas.read_file(r"c:\temp\data_test\point.shp")

output = split_lines(
    line_gdf=line_gdf,
    lid_col='flwpath_id',
    point_gdf=point_gdf,
    tolerance=0.0001,
)

split_failed_gdf = output[output["split"] == "FAILED"]
print(split_failed_gdf)

if len(split_failed_gdf) > 0:
    ax = split_failed_gdf.plot()
    point_gdf.plot(ax=ax, color="red")
    plt.show()
