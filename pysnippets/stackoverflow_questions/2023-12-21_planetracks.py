from pathlib import Path
import geopandas as gpd
import shapely

dir = Path("C:/Temp")
path = dir / "USGS_PaCSEA_GPSdata.csv"

# Maximum and minimum distance to treat as a survey pass
max_pass_distance = 0.1
min_pass_distance = 0.02
min_survey_area = None

df = gpd.read_file(path, engine="pyogrio")
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LON, df.LAT), crs=4326)

# Buffer the input points
buff_gs = gdf.buffer(distance=max_pass_distance / 2)

# Union all the buffered points
buff_union = buff_gs.unary_union
gpd.GeoDataFrame({"geometry": [buff_union]}, crs=4326).to_file(
    dir / "USGS_PaCSEA_GPSdata_buff_diss.gpkg"
)

# Apply negative buffer to remove areas without surveying pattern
buff_union_buff = buff_union.buffer(
    distance=-(max_pass_distance + min_pass_distance) / 2
)
# Positive buffer again, with some margin so outer survey points/lines are retained
survey_zone = buff_union_buff.buffer(distance=min_pass_distance)

# Small zones where single passes cross still need to be removed, e.g. by area.
survey_zones = shapely.get_parts(survey_zone)
survey_zones_gdf = gpd.GeoDataFrame({"geometry": survey_zones}, crs=4326)
survey_zones_gdf.to_file(dir / "USGS_PaCSEA_GPSdata_survey_rois_all.gpkg")

if min_survey_area is None:
    min_survey_area = (max_pass_distance / 2) ** 2 * 3.14
survey_zones_gdf = survey_zones_gdf[survey_zones_gdf.geometry.area > min_survey_area]
survey_zones_gdf.to_file(dir / "USGS_PaCSEA_GPSdata_survey_rois.gpkg")

# Now we can e.g. filter only the points inside the survey zones
survey_gdf = gdf[gdf.intersects(survey_zones_gdf.unary_union)]
survey_gdf.to_file(dir / "USGS_PaCSEA_GPSdata_survey.gpkg")
