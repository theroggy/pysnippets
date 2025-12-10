import logging
from pathlib import Path

import geofileops as gfo


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_dir = Path("//dg3.be/alp/gistmp/dataverwerking/2025-11-13_difference")

    hoogte_paden_path = test_dir / "objecthoogte_classes.gpkg"
    gebouwen_path = Path("X:/GIS/GIS DATA/GRB/GRB2016 (toestand 2016-03-11)/GPKG/gbg.gpkg")
    result_path = test_dir / "hoogte_paden_minus_gebouwen.gpkg"

    gfo.difference(
        input1_path=hoogte_paden_path,
        input2_path=gebouwen_path,
        output_path=result_path,
        # subdivide_coords=0,
        force=True,
    )
