import logging
import geofileops as gfo

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Paths to large polygon files
    seagrass_path = r"C:\Temp\habitat_ocean\WCMC013-014_SeagrassPtPy2021_v7_1\014_001_WCMC013-014_SeagrassPtPy2021_v7_1\01_Data\WCMC013_014_Seagrasses_Py_v7_1.shp"
    saltmarsh_path = r"C:\Temp\habitat_ocean\WCMC027_Saltmarsh_v6_1\WCMC027_Saltmarsh_v6_1\01_Data\WCMC027_Saltmarshes_Py_v6_1.shp"
    output_path = r"C:\Temp\habitat_ocean\intersection_result.gpkg"

    # Compute the intersection
    intersection_gdf = gfo.intersection(
        seagrass_path, saltmarsh_path, output_path, force=True
    )
