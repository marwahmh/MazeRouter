# MazeRouter

Develope a maze router (using python) that implements maze routing algorithm (using A* algorithm). The router connects pins that belong to the same net together using the available routing resources. There are infinite routing layers (M_odd: horizontal and M_even: Vertical) routing grid is 1000x1000 cells foreach layer.

The input to the router is a text file that lists the nets to be routed genrated from the given DEF and LEF files associated with the project.

The shortest path will be given by using g and f, that are used by the A* Algorithm's fuction: f = g + h, where h is the heuristic.
  
The path is also plotted as a 3D graph at the end.

Notes:
- The algorithm minimize the usage of vias (to move between layers), for that high cost is assigned to vias(10). You may route wires vertically on M_odd and horizontally on M_even but do that only when there is no other choice (cost>10).
- The implementation support any number of routing layers. Where we get the maximum number of layers of each net from the DEF and LEF files data.

