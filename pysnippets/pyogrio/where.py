from pathlib import Path
import warnings
import pyogrio

# Ignore all warnings
warnings.simplefilter("ignore")

url_shp = "https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
url_gpkg = (
    "https://github.com/geofileops/geofileops/raw/main/tests/data/polygon-parcel.gpkg"
)
wheres = [
    None,
    "LBLHFDTLT LIKE 'Gras%'",
    "LBLHFDTLT LIKE 'gras%'",
    "LBLHFDTLT ILIKE 'gras%'",
    "LBLHFDTLT NOT LIKE 'Gras%'",
    "LBLHFDTLT != 'Grasklaver'",
    "LBLHFDTLT IN ('Hoofdgebouwen', 'Grasklaver')",
    f"ST_Area({{geometrycolumn}}) > 1000",
]

for where in wheres:
    for url in [url_shp, url_gpkg]:
        for sql_dialect in [None, "OGRSQL", "SQLITE"]:
            where_f = where
            if where is not None:
                geometrycolumn = "geom" if url.endswith(".gpkg") else "geometry"
                where_f = where.format(geometrycolumn=geometrycolumn)
            try:
                df = pyogrio.read_dataframe(url, where=where_f, sql_dialect=sql_dialect)
                print(f"\nnb_rows with where: {where}: {len(df)}")
                print(df["LBLHFDTLT"].unique())
            except Exception as ex:
                name = Path(url).name
                print(
                    f"Error, where={where_f}, sql_dialect={sql_dialect} on {name}"
                )
