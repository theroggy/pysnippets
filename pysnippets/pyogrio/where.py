import pyogrio

url = "https://github.com/theroggy/pysnippets/raw/main/pysnippets/pyogrio/polygon-parcel_31370.zip"
wheres = [
    None,
    "LBLHFDTLT LIKE 'Gras%'",
    "LBLHFDTLT LIKE 'gras%'",
    "LBLHFDTLT ILIKE 'gras%'",
    "LBLHFDTLT NOT LIKE 'Gras%'",
    "LBLHFDTLT != 'Grasklaver'",
    "LBLHFDTLT IN ('Hoofdgebouwen', 'Grasklaver')",
]

for where in wheres:
    df = pyogrio.read_dataframe(url, where=where)
    print(f"\nnb_rows with where: {where}: {len(df)}")
    print(df["LBLHFDTLT"].unique())
