import geopandas as gpd


def main():
    # Data.zip has two shapefiles. DAMSELFISH_distributions.shp and DAMSELFISH_distributions2.shp)
    zipfile_url = "/vsizip/vsicurl/https://github.com/delatitude/spatialtestdata/raw/8c4dea03f4e325aefa523854d44a7084b6316f6e/Data.zip"
    file1_url = f"{zipfile_url}/DAMSELFISH_distributions.shp"
    file2_url = f"{zipfile_url}/DAMSELFISH_distributions2.shp"

    # Source : https://stackoverflow.com/questions/72533355/reading-shapefiles-inside-nested-zip-archives
    gdfs = []
    gdfs.append(gpd.read_file(file1_url))
    gdfs.append(gpd.read_file(file2_url))
    rows, cols = gdfs[-1].shape
    print(f"GeoDataFrame: {rows} rows, {cols} columns\n")

main()
