import geopandas as gpd

df = gpd.read_file(
    "FEATHER:/vsicurl/https://bafybeiabejz3zbxnegvnprjia3gjosgmopzbuf2iacnwdivcs5kgonemsa.ipfs.w3s.link/ipfs/bafybeiabejz3zbxnegvnprjia3gjosgmopzbuf2iacnwdivcs5kgonemsa/national_grazing_allotments.feather",
    engine="pyogrio",
)
