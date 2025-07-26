"""Stackoverflow question.

Reference :https://gis.stackexchange.com/questions/494685/loading-esri-shapefile-having-more-than-10-characters-field-names-in-python#494685
"""

import geopandas as gpd

def suffix_duplicates(strings: list[str]) -> list[str]:
    """Append a suffix to duplicate strings.
    
    Parameters:
    -----------
    strings: a list of strings
        A list of strings with potential duplicates.
    
    Returns:
    --------
    list[str]
        The list of strings with unique names by adding a suffix
        for duplicates.
    """
    unique_strings = []
    string_indexes = {}
    for string in strings:
        if string not in string_indexes:
            string_indexes[string] = 0
        else:
            string_indexes[string] += 1
        if string_indexes[string] > 0:
            unique_strings.append(f"{string}_{string_indexes[string]}")
        else:
            unique_strings.append(string)

    return unique_strings

# Load a shapefile with duplicate column names
path = "https://www.herault-data.fr/api/explore/v2.1/catalog/datasets/trafic-de-l-herault-2023/exports/shp?lang=fr&timezone=Europe%2FBerlin"
gdf = gpd.read_file(path)
print(gdf.columns)

# Rename duplicate column names by appending a suffix
gdf.columns = suffix_duplicates(gdf.columns.tolist())
print(gdf.columns)

# Save the GeoDataFrame again to a shapefile... the new column names
# will be shortened so they become unique within 10 characters.
# Remark: saving a GeoDataFrame with non-unique column names will give an error!
output_path = r"C:\Temp\trafic_de_l_herault_2023.shp"
gdf.to_file(output_path)
written_gdf = gpd.read_file(output_path)
print(written_gdf.columns)
