import re
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("--st_node", type=int, help="start node")
parse.add_argument("--end_node", type=int, help="end node")
arg = parse.parse_args()

def Node2QgisXY(start_node, end_node)
    node_list = []
    with open("sfo_nodes.txt", "r") as file:
        for line in file.readlines():
            node_list.append(line)

    for i in range(len(node_list)):
        node_list[i] = re.split(r'[:<>,\s]', node_list[i].rstrip())

    for i in range(len(node_list)):
        if int(node_list[i][0]) == start_node:
            start_point = (node_list[i][-9], node_list[i][-8])

        if int(node_list[i][0]) == end_node:
            end_point = (node_list[i][-9], node_list[i][-8])

print(start_point, end_point)

