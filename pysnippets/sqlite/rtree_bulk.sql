-- Create test data table
-- ----------------------
-- Load zorder extension
SELECT load_extension('zorder.dll');

--DROP TABLE bboxes;
--DROP TABLE bboxes_rtree;

-- Create table for bboxes
CREATE TABLE bboxes (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  minx FLOAT,
  maxx FLOAT,
  miny FLOAT,
  maxy FLOAT
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

--PRAGMA cache_size=-2000;
--PRAGMA cache_size=-50000;
--PRAGMA cache_size;

-- Create rtree index
CREATE VIRTUAL TABLE bboxes_rtree USING rtree(id, minx, maxx, miny, maxy);

-- Fill up in current order
-- 19.4 s (timings on my laptop on windows)
--INSERT INTO bboxes_rtree SELECT id, minx, maxx, miny, maxy FROM bboxes;

-- Fill up in random order
-- 31.886 s with default cache_size = 2 MB
-- 12.9 s with cache_size = 50 MB
INSERT INTO bboxes_rtree
  SELECT id, minx, maxx, miny, maxy FROM bboxes order by random();

-- Fill up in zorder/morton code order
-- Remark: the DESC sorted insert is faster than random, but I cannot explain why it is
-- that much slower to insert sorted ASC.
-- 15.5 s if ordered ASC
-- 11.6 s if ordered DESC
--INSERT INTO bboxes_rtree
--  SELECT id, minx, maxx, miny, maxy 
--  FROM bboxes order by zorder(minx+(maxx-minx)/2, miny+(maxy-miny)/2) DESC;

-- BULK RTREE TEST
-- ---------------
--DROP TABLE bboxes_rtree_node_bulk;
--DROP TABLE bboxes_rtree_parent_bulk;
--DROP TABLE bboxes_rtree_rowid_bulk;

CREATE TABLE bboxes_rtree_rowid_bulk (
    rowid  INTEGER PRIMARY KEY,
    nodeno INTEGER,
    minx   FLOAT,
    maxx   FLOAT,
    miny   FLOAT,
    maxy   FLOAT
);

CREATE TABLE bboxes_rtree_node_bulk (
    nodeno INTEGER PRIMARY KEY,
    level INTEGER,
    minx   FLOAT,
    maxx   FLOAT,
    miny   FLOAT,
    maxy   FLOAT
);

CREATE TABLE bboxes_rtree_parent_bulk (
    nodeno     INTEGER PRIMARY KEY,
    parentnode INTEGER
);

-- Group leafs per 50 elementes, based on zorder sorting
-- 2.053 s
INSERT INTO bboxes_rtree_rowid_bulk
  SELECT rowid, (row_number() over ()-1)/50+2 as nodeno, minx, maxx, miny, maxy
    FROM (SELECT rowid, * FROM bboxes 
          ORDER BY zorder(minx+(maxx-minx)/2, miny+(maxy-miny)/2)
         );

--DELETE FROM bboxes_rtree_rowid_bulk;
--SELECT nodeno, count(*) nb FROM bboxes_rtree_rowid_bulk group by nodeno order by nb asc;

-- Determine the MBR of the level 0 nodes based on the leaves + insert in 
-- bboxes_rtree_node_bulk
-- 0.537 s
INSERT INTO bboxes_rtree_node_bulk
  SELECT nodeno, 0, min(minx), max(maxx), min(miny), max(maxy)
    FROM bboxes_rtree_rowid_bulk 
   GROUP BY nodeno;

--DELETE FROM bboxes_rtree_node_bulk;

-- Group level 0 nodes per 50 elements ordered by nodeno
-- 0.036 s
INSERT INTO bboxes_rtree_parent_bulk
  SELECT nodeno
        ,(SELECT MAX(nodeno) 
          FROM bboxes_rtree_node_bulk
         ) + (row_number() over ()-1)/50+1 AS parentnode
    FROM (SELECT rowid, * FROM bboxes_rtree_node_bulk
          WHERE level = 0
          ORDER BY nodeno
         );

--DELETE FROM bboxes_rtree_parent_bulk;

-- Determine the MBR of the level 1 nodes based on the level 0 nodes + insert in
-- bboxes_rtree_node_bulk
-- 0.019 s
INSERT INTO bboxes_rtree_node_bulk
  SELECT parentnode, 1, min(minx), max(maxx), min(miny), max(maxy)
    FROM bboxes_rtree_parent_bulk rtree_parent
    JOIN bboxes_rtree_node_bulk rtree_node ON rtree_parent.nodeno = rtree_node.nodeno
   WHERE rtree_node.level = 0
   GROUP BY rtree_parent.parentnode;

--SELECT * FROM bboxes_rtree_node_bulk WHERE level = 1;

-- Group level 1 nodes per 50 elements ordered by nodeno
-- 0.017 s
INSERT INTO bboxes_rtree_parent_bulk
  SELECT nodeno
        ,(SELECT MAX(nodeno) 
          FROM bboxes_rtree_node_bulk
         ) + (row_number() over ()-1)/50+1 as parentnode
    FROM (SELECT rowid, * FROM bboxes_rtree_node_bulk
          WHERE level = 1
          ORDER BY nodeno
         );

-- Determine the MBR of the level 2 nodes based on the level 1 nodes + insert in
-- bboxes_rtree_node_bulk
-- 0.018 s
INSERT INTO bboxes_rtree_node_bulk
  SELECT parentnode, 2, min(minx), max(maxx), min(miny), max(maxy)
    FROM bboxes_rtree_parent_bulk rtree_parent
    JOIN bboxes_rtree_node_bulk rtree_node ON rtree_parent.nodeno = rtree_node.nodeno
   WHERE rtree_node.level = 1
   GROUP BY rtree_parent.parentnode;

-- Determine the MBR of the root node (nodeno 1) + insert in bboxes_rtree_node_bulk
-- 0.011
INSERT INTO bboxes_rtree_node_bulk
  SELECT 1, 3, min(minx), max(maxx), min(miny), max(maxy)
    FROM bboxes_rtree_node_bulk 
   WHERE level = 2;
