import sys
sys.path.append('../graph')
from graph import Graph
from util import Queue, Stack


def earliest_ancestor(ancestors, starting_node):
    flat_ancestors = {item for sublist in ancestors for item in sublist}
    graph = Graph()

    for item in flat_ancestors:
        graph.add_vertex(item)

    for ancestor in ancestors:
        graph.add_edge(ancestor[1], ancestor[0])

    stack = Stack()
    stack.push(starting_node)
    visited = []

    while stack.size() > 0:
        node = stack.pop()
        for items in sorted(graph.vertices[node]):
            stack.push(items)

        if node not in visited and node != starting_node:
            visited.append(node)

    if len(visited) < 1:
        return -1
    return visited[-1]
