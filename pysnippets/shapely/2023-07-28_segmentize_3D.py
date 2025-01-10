import shapely

line = shapely.LineString([(0, 0, 0), (1, 10, 2)])
line_seg = shapely.segmentize(line, 1)
print(line_seg)
# output: LINESTRING Z (0 0 0, 0.0909090909090909 0.9090909090909092 0.1818181818181818, 0.1818181818181818 1.8181818181818183 0.3636363636363636, 0.2727272727272728 2.7272727272727275 0.5454545454545455, 0.3636363636363636 3.6363636363636367 0.7272727272727273, 0.4545454545454546 4.545454545454546 0.9090909090909092, 0.5454545454545455 5.454545454545455 1.090909090909091, 0.6363636363636364 6.363636363636363 1.2727272727272727, 0.7272727272727273 7.272727272727273 1.4545454545454546, 0.8181818181818182 8.181818181818182 1.6363636363636365, 0.9090909090909092 9.090909090909092 1.8181818181818183, 1 10 2)
