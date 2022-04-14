from random import random, choice

# lots of optimization can be done. However, performance is adequite,
# for my purposes (up to 250 is ok.).
# main culprit is search_patcher which only adds a single node each iteration.

# sacrificing some randomness by tieing together identified partisions increases
# performance drastically.


def random_undirected_graph(num_nodes):
    vertices = [x for x in range(num_nodes)]
    edges = {}

    # construct original directed graph with random edges.
    for v in vertices:
        edges[v] = []
        for n in vertices:
            if n == v:
                continue
            p = random() < 1.0 / len(vertices)
            if p:
                edges[v].append(n)

    # connects a partitioned graph.
    graph = _search_patch(edges)

    # to undirected graph.
    for v, es in graph.items():
        for e in es:
            if v not in graph[e]:
                graph[e].append(v)

    return graph


def random_directed_graph(num_nodes):
    undirected_graph = random_undirected_graph(num_nodes)

    # remove random edges such that the graph becomes directed.
    for v, neighs in undirected_graph.items():
        for e in neighs:
            if not v in undirected_graph[e]:
                continue  # already removed backward edge
            if random() > .5:  # introduce some randomness in deletion.
                undirected_graph[e].remove(v)
            else:
                undirected_graph[v].remove(e)
    return undirected_graph


def _search_patch(graph):
    """
    patches partition by performing graph search. If partitions are detected,
    a random edge is inserted and the procedure is called upon once again.
    extremely ineffeicient but decent for randomness.
    """
    vertices = list(graph.keys())
    while True:
        v = choice(vertices)
        neighbours = [v]
        visited = []
        # check whether all nodes may be reached.
        while len(neighbours) > 0:
            curr = neighbours.pop()
            visited.append(curr)
            neighbours = neighbours + graph[curr]
            neighbours = list(filter(lambda a: not a in visited, neighbours))

        # if lengths are equal then the graph is connected.
        if len(visited) == len(graph):
            return graph

        # creating a connection between the searched set and a missing node.
        unconnected = list(filter(lambda a: not a in visited, vertices))
        random_unconnected = choice(unconnected)
        random_connected = choice(visited)

        # undirected connection
        graph[random_unconnected].append(random_connected)
        graph[random_connected].append(random_unconnected)
