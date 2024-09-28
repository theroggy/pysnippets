from pathlib import Path
from owslib.wfs import WebFeatureService
import geopandas as gpd

# Save the WFS response to a .gml file so a .gfs file is saved once 
# it is read with `read_file`.
path = Path("c:/temp/VerwaltungsEinheit.gml")
if not path.exists():

    wfs = WebFeatureService(url="https://dienste.gdi-sh.de/WFS_SH_ALKIS_VWG_OpenGBD", version="2.0.0", timeout=180)
    response = wfs.getfeature(typename="ave:VerwaltungsEinheit")
    with open(path, "wb") as f:
        f.write(response.getbuffer())

    print(gpd.read_file(path).dtypes)


# Read directly from the WFS response, but specify the .gfs template to specify
# the data types.
from owslib.wfs import WebFeatureService
import geopandas as gpd

wfs = WebFeatureService(url="https://dienste.gdi-sh.de/WFS_SH_ALKIS_VWG_OpenGBD", version="2.0.0", timeout=180)
response = wfs.getfeature(typename="ave:VerwaltungsEinheit")

print(
    gpd.read_file(
        wfs.getfeature(typename="ave:VerwaltungsEinheit"),
        GFS_TEMPLATE="C:/Temp/VerwaltungsEinheit.gfs"
    ).dtypes, 
)
