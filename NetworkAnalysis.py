from qgis.core import (
  QgsVectorLayer,
  QgsPointXY,
)
import re
import argparse
import time
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *


def Node2QgisXY(start_node, end_node):
    node_list = []
    with open("sfo_nodes.txt", "r") as file:
        for line in file.readlines():
            node_list.append(line)

    for i in range(len(node_list)):
        node_list[i] = re.split(r'[:<>,\s]', node_list[i].rstrip())

    for i in range(len(node_list)):
        if int(node_list[i][0]) == start_node:
            start_point = (float(node_list[i][-9]), float(node_list[i][-8]))

        if int(node_list[i][0]) == end_node:
            end_point = (float(node_list[i][-9]), float(node_list[i][-8]))
    return start_point, end_point
parse = argparse.ArgumentParser()
parse.add_argument("--start_node", type=int, help="start node")
parse.add_argument("--end_node", type=int, help="end node")
parse.add_argument("--path_output", help="specify the shortest path for output file")
parse.add_argument("--status_output", help="specify the status path for output file")
arg = parse.parse_args()

start = time.time()
vectorLayer = QgsVectorLayer('./data-shape|layername=sfo_roads', 'lines')
director = QgsVectorLayerDirector(vectorLayer, -1, '', '', '', QgsVectorLayerDirector.DirectionBoth)
strategy = QgsNetworkDistanceStrategy()
director.addStrategy(strategy)

builder = QgsGraphBuilder(vectorLayer.sourceCrs())
start_point, end_point = Node2QgisXY(arg.start_node, arg.end_node)
print(start_point, end_point)

startPoint = QgsPointXY(start_point[0], start_point[1])
endPoint = QgsPointXY(end_point[0], end_point[1])

tiedPoints = director.makeGraph(builder, [startPoint, endPoint])
tStart, tStop = tiedPoints

graph = builder.graph()
idxStart = graph.findVertex(tStart)
idxEnd = graph.findVertex(tStop)

(tree, costs) = QgsGraphAnalyzer.dijkstra(graph, idxStart, 0)

if tree[idxEnd] == -1:
    raise Exception('No route!')

# Total cost
cost = costs[idxEnd]

# Add last point
route = [graph.vertex(idxEnd).point()]

# Iterate the graph
while idxEnd != idxStart:
    idxEnd = graph.edge(tree[idxEnd]).fromVertex()
    route.insert(0, graph.vertex(idxEnd).point())

# Display in the Qgis
# rb = QgsRubberBand(iface.mapCanvas())
# rb.setColor(Qt.red)
#
# # This may require coordinate transformation if project's CRS
# # is different than layer's CRS
# for p in route:
#     rb.addPoint(p)
end = time.time()

with open(arg.path_output, 'w') as file:
    file.write("node {} to node {}\n".format(arg.start_node, arg.end_node))
    for line in route:
        file.write(str(line))
        file.write("\n")

with open(arg.status_output, "w") as file:
    file.write('node {} to node {} spent {}s to compute'.format(arg.start_node, arg.end_node, (end - start)))