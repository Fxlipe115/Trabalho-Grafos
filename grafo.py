#!/usr/bin/python3
import argparse
import operator
import collections


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]


def read_file(file_path):
    graph = SimpleGraph()
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
            for node in line:
                try:
                    if graph.edges[line[0]]:
                        graph.edges[line[0]].append(node)
                except KeyError:
                    if node is not line[0]:
                        graph.edges.update({line[0]:[node]})

    return graph

def breadth_search(graph, start):
    frontier = Queue()
    frontier.put(start)
    visited = {}
    visited[start] = True

    while not frontier.empty():
        current = frontier.get()
        print("Visiting %r" % current)
        for next in graph.neighbors(current):
            if next not in visited:
                frontier.put(next)
                visited[next] = True

    return visited

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
    GRAPH = read_file(FILENAME)
    comp = []
    print('Graph:')
    print(GRAPH.edges)

    for key in GRAPH.edges:
        print(key + ':')
        visited = breadth_search(GRAPH, key)
        comp.append(list(visited.keys()))
        print()
    print(comp)
