import geopandas as gpd
import requests

wfs_url = "https://kartta.hel.fi/ws/geoserver/avoindata/wfs"
layer = "avoindata:Opaskartta_alueenviiva"
params = dict(
    service="WFS",
    version="1.0.0",
    request="GetFeature",
    typeName=layer,
    outputFormat="json",
    startIndex=33000,
    count=100,
)
r = requests.Request("GET", wfs_url, params=params).prepare()

data = gpd.read_file(r.url)
print(data)
