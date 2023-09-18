select load_extension('zorder.dll');

-- Create table for bboxes
CREATE TABLE bboxes_zorder (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  minx FLOAT,
  maxx FLOAT,
  miny FLOAT,
  maxy FLOAT,
  zorder FLOAT
);

-- Fill the table with 1 million bboxes
INSERT INTO bboxes(minx, maxx, miny, maxy)
  WITH RECURSIVE
    cnt(x) AS (
       SELECT 0
       UNION ALL
       SELECT x+10 FROM cnt
        LIMIT 1000
    )
  SELECT minx, maxx, miny, maxy
    FROM (SELECT x AS minx, x+10 AS maxx FROM cnt) x,
         (SELECT x AS miny, x+10 AS maxy FROM cnt) y;

PRAGMA cache_size=-2000;
PRAGMA cache_size=-50000;
PRAGMA cache_size;

-- Create and fill up rtree.
CREATE VIRTUAL TABLE bboxes_rtree USING rtree(id, minx, maxx, miny, maxy);

-- 19.4 s
INSERT INTO bboxes_rtree
  SELECT id, minx, maxx, miny, maxy FROM bboxes;

-- 31.886 s
-- 12.9 s met 50 MB cache
INSERT INTO bboxes_rtree
  SELECT id, minx, maxx, miny, maxy FROM bboxes order by random();

-- 26 s met 2 MB cache
-- 20.4 s met 50 MB cache
INSERT INTO bboxes_rtree
  SELECT id, minx, maxx, miny, maxy FROM bboxes order by zorder(minx, miny);

-- 11.6 s
INSERT INTO bboxes_rtree
  SELECT id, minx, maxx, miny, maxy FROM bboxes order by zorder(minx+(maxx-minx)/2, miny+(maxy-miny)/2) DESC;

DROP table bboxes_rtree;

-- BULK RTREE TEST
CREATE TABLE bboxes_rtree_node_bulk (
    nodeno INTEGER PRIMARY KEY,
    level INTEGER,
    data
);

CREATE TABLE bboxes_rtree_parent_bulk (
    nodeno     INTEGER PRIMARY KEY,
    parentnode INTEGER
);

CREATE TABLE bboxes_rtree_rowid_bulk (
    rowid  INTEGER PRIMARY KEY,
    nodeno INTEGER
);

INSERT INTO bboxes_rtree_rowid_bulk
  SELECT rowid, (row_number() over ()-1)/50+1 as nodeno from bboxes order by zorder(minx+(maxx-minx)/2, miny+(maxy-miny)/2);

delete from bboxes_rtree_rowid_bulk;

select nodeno, count(*) nb from bboxes_rtree_rowid_bulk group by nodeno order by nb asc;

INSERT INTO bboxes_rtree_parent_bulk
  SELECT rowid, nodeno from bboxes_rtree_rowid_bulk;

delete from bboxes_rtree_parent_bulk;
