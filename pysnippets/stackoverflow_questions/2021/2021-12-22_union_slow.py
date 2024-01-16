    from pathlib import Path
    import geofileops as gfo
    import logging

    logging.basicConfig(level=logging.INFO)
    input_path = Path("C:/Temp/sample_geodata.gpkg")
    output_path = input_path.parent / "sample_geodata_union.gpkg"

    gfo.union(
        input1_path=input_path,
        input2_path=input_path,
        output_path=output_path,
        input1_layer="layer1_forest",
        input2_layer="layer2_parcel",
        force=True,
    )
