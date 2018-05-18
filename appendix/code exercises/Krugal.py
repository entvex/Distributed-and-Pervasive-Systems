#! /usr/bin/python

import networkx as nx
import matplotlib.pyplot as plot

nodes = [0, 1, 2, 3, 4]
edges = [(0,1,{"weight": 1}),
         (0,2,{"weight": 3}),
         (0,3,{"weight": 6}),
         (0,4,{"weight": 7}),
         (1,2,{"weight": 2}),
         (1,3,{"weight": 5}),
         (3,2,{"weight": 8}),
         (3,4,{"weight": 4}),
         (2,2,{"weight": 1})]

print "Nodes: {0}. Edges: {1}".format(len(nodes), len(edges))



graph = nx.Graph()
graph.add_nodes_from(nodes)

for (a,b,w) in edges:
    weight = w["weight"]
    if a != b:
        if graph.has_edge(a,b):
            e = graph.edges[a,b]
            print "weights: {0} vs {1}".format(w,e)
            graph.add_edges_from([(a, b, {"weight": min(w["weight"], e["weight"])})])
        else:
            graph.add_edges_from([(a,b,{"weight": weight})])


sorted_edges = sorted(graph.edges(data=True), key=lambda x: x[2]["weight"])

result = nx.Graph()
result.add_nodes_from(nodes)

for (a,b,w) in sorted_edges:
    if not nx.has_path(result, a, b):
        result.add_edges_from([(a, b, {"weight":w})])

print "sorted edges: \n {}".format(sorted_edges)

#nx.draw(graph, with_labels=True, font_weight="bold")
print "graph includes {} edges".format(len(graph.edges))
plot.subplot(221)

#nx.draw(result, with_labels=True, font_weight="bold")
print "result includes {} edges".format(len(result.edges))
print "results edges {}".format(result.edges)
plot.subplot(241)

plot.show()

#(a1 == a2 ^ b1 == b2) v (a1 == b2 ^ b1 == a2)
