from pathlib import Path
import geofileops as gfo
import logging

if __name__ == "__main__":
    # Init logging to have progress logging
    logging.basicConfig(level=logging.INFO)

    input_path = Path("C:/Temp/input.gpkg")
    output_path = input_path.parent / "output.gpkg"

    gfo.union(input1_path=input_path, input2_path=None, output_path=output_path)
