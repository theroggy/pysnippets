import os

os.system(
    r'ogr2ogr -f "GeoJSON" "C:\Users\Gebruiker\Documents\GitHub\pysnippets\pysnippets\stackoverflow_questions\2024\Q3\2024-09-02_psv.geojson" "C:\Users\Gebruiker\Documents\GitHub\pysnippets\pysnippets\stackoverflow_questions\2024\Q3\2024-09-02_psv.psv" -oo SEPARATOR=PIPE -oo GEOM_POSSIBLE_NAMES=geom'
)
