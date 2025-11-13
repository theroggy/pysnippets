from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

import geopandas as gpd
from tqdm import tqdm

if __name__ == "__main__":
    data_dir = Path("C:/temp/ALKIS-Brandenburg")
    vector_files = list(data_dir.rglob(f"**/*.zip"))

    filename = "Flurstueck.shp"
    vector_files = [f"/vsizip/{(f / filename).as_posix()}" for f in vector_files]

    with ProcessPoolExecutor(max_workers=4) as executor:
        gdfs = list(tqdm(executor.map(gpd.read_file, vector_files), total=len(vector_files), smoothing=0.1))

    # Use GeoPandas concat to preserve geometry properly
    merged_gdf = gpd.pd.concat(gdfs, ignore_index=True)

    merged_gdf.to_file(data_dir / "merged.gpkg")
