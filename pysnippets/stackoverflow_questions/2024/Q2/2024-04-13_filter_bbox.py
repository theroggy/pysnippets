from pathlib import Path
import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import box, Point
from shapely.ops import transform

bounding_box = {
    "min_lon": 12.927785560520098,
    "max_lon": 13.94903874307725,
    "min_lat": 52.284843473119714,
    "max_lat": 52.77168805093944,
}

min_lon = bounding_box["min_lon"]
max_lon = bounding_box["max_lon"]
min_lat = bounding_box["min_lat"]
max_lat = bounding_box["max_lat"]

# Convert bbox to crs of data: epsg:3857
transformer = Transformer.from_crs(4326, 3857)
min_3857 = transform(transformer.transform, Point(min_lat, min_lon))
max_3857 = transform(transformer.transform, Point(max_lat, max_lon))

dir = Path("C:/Temp/test_population")
# dir = Path("C:/Users/Julian/Downloads/kontur_population.gpkg")
data = gpd.read_file(
    dir / "kontur_population_20231101.gpkg",
    bbox=(min_3857.x, min_3857.y, max_3857.x, max_3857.y),
    engine="pyogrio",
)

bbox = box(min_3857.x, min_3857.y, max_3857.x, max_3857.y)
clipped_data = data.loc[data.geometry.within(bbox)]
clipped_data.to_file(
    dir / "kontur_population_within.gpkg",
    driver="GPKG",
    engine="pyogrio",
)
