from datetime import datetime, timedelta
from pathlib import Path
import geopandas as gpd
from urllib.error import HTTPError


# Some variables to fill out
wfs_url = (
    "https://inspirepub.waterinfo.be/arcgis/services/"
    "WFS_overstromingsgevoelige_gebieden/MapServer/WFSServer?"
)
layernames = (
    "WFS_overstromingsgevoelige_gebieden:overstromingsgevoelige_gebieden_pluviaal"
)
# Optional: number of features to be fetched (only used for progress reporting)
nb_features = 16704620
count = 10000
startindex = 0

output_dir = Path("C:/temp")
output_path = output_dir / "pluviaal_py.gpkg"
append = False

# Now we can start loading the data
if output_path.exists() and not append:
    raise ValueError(f"output_path exists:{output_path}")

nb_batches = (nb_features - startindex) / count if nb_features is not None else None
nb_batches_done = 0
start_time = datetime.now()
eta = ""
retry_count_max = 10
while True:
    # Fetch page
    page_url = (
        f"{wfs_url}SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&"
        f"TYPENAMES={layernames}&STARTINDEX={startindex}&COUNT={count}"
    )
    retry_count = 0
    data = None
    while retry_count < retry_count_max:
        try:
            data = gpd.read_file(page_url)
        except HTTPError as ex:
            if str(ex) == "HTTP Error 400: Bad Request":
                retry_count += 1
                print(f"Error {ex}, retry nb {retry_count} for {page_url}")
                continue
            raise ex

    assert data is not None and isinstance(data, gpd.GeoDataFrame)
    data.to_file(output_path, engine="pyogrio", append=True)
    nb_batches_done += 1
    if nb_batches is not None:
        sec_per_batch = (datetime.now() - start_time).total_seconds()
        nb_todo = nb_batches - nb_batches_done
        eta = f", time left: {timedelta(seconds=nb_todo * sec_per_batch)}"
    print(f"Succesful save of page with startindex {startindex}, count: {count}{eta}")

    if len(data) < count:
        print(f"Only {len(data)} rows returned instead of count, so probably ready...")
        break

    startindex += count
