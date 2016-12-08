#!/usr/bin/python3
import argparse
import operator


class Node(object):
    '''
    Represents a node in the graph.

    Input:
    name: string = name of the node
    '''

    def __init__(self, name):
        """
        Class constructor.
        """
        self.name = str(name)
        self.flag = 0

    def __repr__(self):
        """
        __repr__ method override.
        """
        return self.name


class Edge(object):
    """
    Represents an edge in the graph.

    Inputs:
    start:Node = start node of the edge
    end:Node = end node of the edge
    """

    def __init__(self, start, end):
        """
        Class constructor.
        """
        self.start = Node(start)
        self.end = Node(end)
        self.name = str(self)

    def __repr__(self):
        """
        __repr__ method override.
        """
        return str(self.start) + '-' + str(self.end)


def read_file(file_path):
    nodes = []
    edges = []
    for line in open(file_path):
        try:
            if int(line):
                line = ''
        except ValueError:
            pass
        line = line.replace(")", '')
        line = line.replace("(", '')
        line = line.split()
        if line:
            nodes.append(line[0])
            for node in line:
                if node is not line[0]:
                    edges.append(Edge(line[0], node))

    return nodes, sorted(edges, key=operator.attrgetter('name'))


def find_path(graph, start, end, path=[]):
    """
    graph:tuple = the graph.
    start:string = start node.
    end:string = end node.
    """
    path += [start]
    if start == end:
        return path
    if not start in graph[0]:
        return None
    for edge in graph[1]:
        if edge.start.name == start and edge.end.name not in path:
            newpath = find_path(graph, edge.end.name, end, path)
            if newpath:
                return newpath
    return None

if __name__ == '__main__':
    PRS = argparse.ArgumentParser(description='Trabalho de Grafos 2016/2'
                                  + '\n\tArthur Zachow Coelho'
                                  + '\n\tFelipe de Almeida Graeff'
                                  + '\n\tHenrique Barboza',
                                  formatter_class=argparse.RawTextHelpFormatter)
    PRS.add_argument('-f', dest='file', required=True, help='The graph file.')
    ARGS = PRS.parse_args()
    FILENAME = ARGS.file
    NODES, EDGES = read_file(FILENAME)
    GRAPH = (NODES, EDGES)
    print('Graph:')
    print(GRAPH)
    componente = []
    for node in GRAPH[0]:
        for node1 in list(reversed(GRAPH[0])):
            if find_path(GRAPH, node, node1) and find_path(GRAPH, node1, node):
                componente.append(node)
                componente.append(node1)
    print(list(set(componente)))
    """print('Path:')
    print(find_path(GRAPH, '1', '3'))"""
