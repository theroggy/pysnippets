from pathlib import Path
import os

out_path = Path("out.geojson")
if out_path.exists():
    out_path.unlink()
cmds = []

# gpkg
cmds.append(
    (
        "test1",
        r"""ogr2ogr -sql "SELECT * FROM parcels WHERE LBLHFDTLT ILIKE 'gras%'" -dialect OGRSQL out.geojson "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"
""",
    )
)

cmds.append(
    (
        "test1",
        r"""ogr2ogr -sql "SELECT * FROM parcels WHERE LBLHFDTLT ILIKE 'gras%'" -dialect OGRSQL out.geojson C:\Users\Gebruiker\Documents\GitHub\geofileops\tests\data\polygon-parcel.gpkg
""",
    )
)

cmds.append(
    (
        "test1",
        r"""ogr2ogr -sql "SELECT LBLHFDTLT FROM parcels WHERE LBLHFDTLT ILIKE 'gras%'" -dialect OGRSQL out.geojson C:\Users\Gebruiker\Documents\GitHub\geofileops\tests\data\polygon-parcel.gpkg
""",
    )
)

cmds.append(
    (
        "test1",
        r"""ogr2ogr -where "LBLHFDTLT ILIKE 'gras%'" -dialect OGRSQL out.geojson C:\Users\Gebruiker\Documents\GitHub\geofileops\tests\data\polygon-parcel.gpkg
""",
    )
)

# shapefile
cmds.append(
    (
        "test1",
        r"""ogr2ogr -where "LBLHFDTLT ILIKE 'gras%'" -dialect OGRSQL out.geojson "/vsizip//vsicurl/https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
""",
    )
)

cmds.append(
    (
        "test1",
        r"""ogr2ogr -where "LBLHFDTLT ILIKE 'gras%'" -dialect SQLITE out.geojson "/vsizip//vsicurl/https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
""",
    )
)

cmds.append(
    (
        "test1",
        r"""ogr2ogr -sql "SELECT * FROM \"polygon-parcel_31370\" WHERE LBLHFDTLT ILIKE 'gras%'" -dialect SQLITE out.geojson "/vsizip//vsicurl/https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
""",
    )
)

for test, cmd in cmds:
    print(f"--- test {test} ---")
    res = os.system(cmd)
