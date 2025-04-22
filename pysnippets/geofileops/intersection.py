import logging

import geofileops as gfo

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    input1_path = r"C:\Temp\polygon_parcel\polygon-parcel.gpkg"
    input2_path = r"C:\Temp\prc2023\prc2023.gpkg"
    output_path = r"C:\Temp\polygon_parcel\output_intersection.gpkg"

    gfo.intersection(input1_path, input2_path, output_path)
