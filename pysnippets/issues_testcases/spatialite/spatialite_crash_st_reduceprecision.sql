SELECT * FROM "130_diss_bufp_diss_bufm";

-- Returns 16 which is a bit weird, but it isn't 0 so OK I suppose.
SELECT ST_IsEmpty(geom) FROM "130_diss_bufp_diss_bufm";

SELECT ST_NPoints(geom) FROM "130_diss_bufp_diss_bufm";

SELECT ST_AsText(geom) FROM "130_diss_bufp_diss_bufm";

SELECT ST_Intersection(geom, ST_Point(0, 1)) FROM "130_diss_bufp_diss_bufm";

SELECT ST_Buffer(geom, 1) FROM "130_diss_bufp_diss_bufm";

-- Crash!
SELECT ST_ReducePrecision(geom, 0.001) FROM "130_diss_bufp_diss_bufm";
