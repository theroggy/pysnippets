import geopandas as gpd
from matplotlib import pyplot as plt
import shapely

railway = gpd.read_file(
    "https://data.ibb.gov.tr/tr/dataset/8b8603dd-2642-4789-a891-4bb7cb2c94e8/resource/ba2ab5a2-32f4-4989-a2c5-99c15c066eb5/download/2022-yl-rayl-ulam-hatlar-vektor-verisi.csv",
)
railway = railway.drop(columns=["field_7", "field_8", "geometry"])
# Since geopandas didn't understand GEOMETRY column as its geometry, I've dropped it.
railway = railway.rename(columns={"GEOMETRY": "geometry"})
# railway['geometry'] = gpd.GeoSeries.from_wkt(railway['geometry'])


def clean_geometrylist_LineString(coordinates):
    cleaned_coordinates = []
    for coord in coordinates:
        lat_lon = coord.split()
        if len(lat_lon) == 2:
            cleaned_coordinates.append([float(lat_lon[0]), float(lat_lon[1])])
        elif len(lat_lon) == 3:
            if "(" in lat_lon:
                lat_lon.remove("(")
            elif ")" in lat_lon:
                lat_lon.remove(")")
            else:
                raise SyntaxError("Look up!!!!!!!!!!")
            cleaned_coordinates.append([float(lat_lon[0]), float(lat_lon[1])])
    return cleaned_coordinates


def clean_geometry(geometry_string):
    geom_type = geometry_string[: geometry_string.index("(")]
    geometry_string = geometry_string.replace(geom_type, "")
    geometry_string = geometry_string.replace("(", "(,")
    geometry_string = geometry_string.replace(")", ",)")
    coordinates = geometry_string.split(",")

    if geom_type == "LINESTRING ":
        cleaned_coordinates = clean_geometrylist_LineString(coordinates)
        clean_geo = shapely.LineString(cleaned_coordinates)
    elif geom_type == "MULTILINESTRING ":
        cleaned_coordinates = clean_geometrylist_LineString(coordinates)
        clean_geo = shapely.LineString(cleaned_coordinates)

    return clean_geo

print(railway['geometry'].str.len())
railway["geometry"] = railway["geometry"].apply(clean_geometry)
railway = gpd.GeoDataFrame(railway, geometry="geometry")

railway.clip([300000, 4510000, 500000, 5000000]).plot()
plt.show()
