#!/bin/env python

import sys
from connected_graph import random_directed_graph
from graphviz import Digraph
from getopt import getopt


def make_graph(num_nodes, format, filename):
    graph = random_directed_graph(num_nodes)
    vertices = list(graph.keys())

    dot = Digraph(filename=filename, format=format)

    for v in vertices:
        dot.node(f"P{v}", f"P{v}", shape="circle")
    sinkNode= f"P{vertices[len(vertices)-1]}"
    dot.node(sinkNode, sinkNode, shape='doublecircle')

    for v, e in graph.items():
        for n in e:
            dot.edge(f"P{v}", f"P{n}")
    return dot


def main(argv):
    args, _ = getopt(argv, 'o:f:v:')
    vertices = 50
    format = 'svg'
    filename = 'out'
    for opt, arg in args:
        if opt == '-f':
            format = arg
        elif opt == '-o':
            filename = arg
        elif opt == '-v':
            try:
                vertices = int(arg)
            except:
                print(f"could parse {arg} as an integer")
                exit(1)
        else:
            print(f"unknown option {opt} with argument {arg}")
            exit(1)
    
    make_graph(vertices, format, filename).render()


if __name__ == '__main__':
    main(sys.argv[1:])
