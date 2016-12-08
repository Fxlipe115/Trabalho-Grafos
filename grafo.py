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

import sys
import time
import resource
from itertools import groupby
from collections import defaultdict
 
 
#set rescursion limit and stack size limit
sys.setrecursionlimit(10 ** 6)
resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, 2 ** 30))

class Track(object):
    """Keeps track of the current time, current source, component leader,
    finish time of each node and the explored nodes."""

    def __init__(self):
        self.current_time = 0
        self.current_source = None
        self.leader = {}
        self.finish_time = {}
        self.explored = set()

def dfs(graph_dict, node, track):
    """Inner loop explores all nodes in a SCC. Graph represented as a dict,
    {tail node: [head nodes]}. Depth first search runs recrusively and keeps
    track of the parameters"""

    track.explored.add(node)
    track.leader[node] = track.current_source
    for head in graph_dict[node]:
        if head not in track.explored:
            dfs(graph_dict, head, track)
    track.current_time += 1
    track.finish_time[node] = track.current_time


def dfs_loop(graph_dict, nodes, track):
    """Outter loop checks out all SCCs. Current source node changes when one
    SCC inner loop finishes."""

    for node in nodes:
        if node not in track.explored:
            track.current_source = node
            dfs(graph_dict, node, track)


def scc(graph, reverse_graph, nodes):
    """First runs dfs_loop on reversed graph with nodes in decreasing order,
    then runs dfs_loop on orignial graph with nodes in decreasing finish
    time order(obatined from firt run). Return a dict of {leader: SCC}."""

    out = defaultdict(list)
    track = Track()
    dfs_loop(reverse_graph, nodes, track)
    sorted_nodes = sorted(track.finish_time,
                          key=track.finish_time.get, reverse=True)
    track.current_time = 0
    track.current_source = None
    track.explored = set()
    dfs_loop(graph, sorted_nodes, track)
    for lead, vertex in groupby(sorted(track.leader, key=track.leader.get),
                                key=track.leader.get):
        out[lead] = list(vertex)
    return out

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
                    graph.edges[int(line[0])].append(int(node))
                except KeyError:
                    if node is not line[0]:
                        graph.edges.update({int(line[0]):[int(node)]})

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
    rev = {
        0: [],
        1: [0, 3],
        2: [5],
        3: [4],
        4: [1],
        5: [2, 4]
    }

    comp = []
    print('Graph:')
    print(GRAPH.edges)
    print(scc(GRAPH.edges, rev, [0, 1, 2, 3, 4, 5]))
"""
    for key in GRAPH.edges:
        print(key + ':')
        visited = breadth_search(GRAPH, key)
        comp.append(list(visited.keys()))
        print()
    print(comp)
"""
