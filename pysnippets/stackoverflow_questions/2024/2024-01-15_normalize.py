import geopandas as gpd
from matplotlib import pyplot as plt
import shapely
from shapely.affinity import scale, translate
from shapely.plotting import plot_polygon


def normalize_polygon_file(polygon_shapefile, output_shapefile):
    """
    Normalizes the coordinates of the polygon to fit within a 0 to 1 range.

    :param polygon_shapefile: Path to the input polygon shapefile.
    :param output_shapefile: Path for the output shapefile with the normalized polygon.
    """
    # Read the original polygon shapefile
    polygon_gdf = gpd.read_file(polygon_shapefile)

    # Assuming there's only one polygon in the shapefile
    original_polygon = polygon_gdf.geometry[0]
    normalized_polygon = normalize_geometry(original_polygon)

    # Replace the geometry of the polygon with the normalized one
    polygon_gdf.geometry = [normalized_polygon]

    # Save the new polygon to a shapefile
    polygon_gdf.to_file(output_shapefile)


def normalize_geometry(geometry):
    """
    Normalizes the coordinates of the geometry to fit within a 0 to 1 range.

    :param geometry: geometry to normalize.
    """
    # Translate the polygon to the origin (0,0)
    translated_polygon = translate(
        geometry,
        xoff=-geometry.bounds[0],
        yoff=-geometry.bounds[1],
    )

    # Calculate scale factors to normalize coordinates between 0 and 1
    x_scale = 1 / (geometry.bounds[2] - geometry.bounds[0])
    y_scale = 1 / (geometry.bounds[3] - geometry.bounds[1])

    # Scale the polygon
    return scale(translated_polygon, xfact=x_scale, yfact=y_scale, origin=(0, 0))


test_poly = shapely.box(
    50.000015366212533729156,
    50.000015366212533729156,
    104.511257929003152,
    80.511257929003152,
)
plot_polygon(test_poly)
plt.show()

normalized = normalize_geometry(test_poly)
print(normalized)
plot_polygon(normalized)

plt.show()
