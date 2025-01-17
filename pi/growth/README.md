# Growth algorithm

This directory contains an algorithm for logically connecting a series of points.

Point
- init(x, y, id)

Cluster
- init()
- register(point)
- register_e(point)
- drop_depth(cutoff) -> List of dropped points
- grow()
- format_lines() -> List of segments formatted for matplotlib
- export_cluster(jsonfilename)
- import_cluster(jsonfilename)
