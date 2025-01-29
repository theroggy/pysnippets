import logging

import geofileops as gfo
import pygeoops

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    le = r"X:\GIS\GIS DATA\Landschapselementen\LandschapsElementenLV_status2013-2015\Cijferwebsite (publicatie)\Landschapselementen_rond_binnen_landbouwgebruikspercelen_2017.gpkg"
    le_centerlines = r"c:\temp\centerlines.gpkg"

    # Disable densify for this dataset, otherwise error:
    #     `GEOSException: Tolerance is too small compared to geometry length`
    gfo.apply(
        input_path=le,
        output_path=le_centerlines,
        func=lambda geom: pygeoops.centerline(geom, densify_distance=0),
        batchsize=10000,
    )
