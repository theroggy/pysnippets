import geopandas as gpd
from matplotlib import pyplot as plt
import shapely
import shapely.plotting
from shapely import get_parts, get_coordinates, LineString, Point

# Inputput data and parameters
url = "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"
polys = gpd.read_file(url)
polys = polys.loc[~polys.is_empty]
xmin, ymin, xmax, ymax = polys.total_bounds
poi = Point(156800, 196700)

# Find largest possible candidate for roi
lines = gpd.GeoDataFrame(
    {
        "descr": ["right", "bottom", "left", "top"],
        "geometry": [
            LineString([poi, Point(xmax, poi.y)]),
            LineString([poi, Point(poi.x, ymin)]),
            LineString([poi, Point(xmin, poi.y)]),
            LineString([poi, Point(poi.x, ymax)]),
        ],
    },
    crs=polys.crs,
)
lines_dif = lines.overlay(polys, "difference", keep_geom_type=True)
roi_xmin = get_coordinates(get_parts(lines_dif.loc[lines_dif.descr == "left"].geometry)[0])[1][0]
roi_ymin = get_coordinates(get_parts(lines_dif.loc[lines_dif.descr == "bottom"].geometry)[0])[1][1]
roi_xmax = get_coordinates(get_parts(lines_dif.loc[lines_dif.descr == "right"].geometry)[0])[1][0]
roi_ymax = get_coordinates(get_parts(lines_dif.loc[lines_dif.descr == "top"].geometry)[0])[1][1]
roi_max = shapely.box(roi_xmin, roi_ymin, roi_xmax, roi_ymax)

# Now start looking for the largest roi without intersections


# Plot
fig, ax = plt.subplots()
polys.plot(ax=ax)
lines.plot(ax=ax, color="red")
shapely.plotting.plot_polygon(roi_max, ax=ax, color="green")
plt.show()
