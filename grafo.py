#!/usr/bin/python3
import argparse
from collections import deque
import operator
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

def reverse_graph(graph, nodes):
    """
    Reverses the directed graph.
    """
    edges = set()
    new_graph = dict()
    for node,dest_nodes in graph.items():
        for dest_node in dest_nodes:
            edges.add((node, dest_node))
    for edge in edges:
        dest_nodes = new_graph.get(edge[1],set())
        dest_nodes.add(edge[0])
        new_graph[edge[1]] = dest_nodes
    for node in nodes:
        if node not in new_graph.keys():
            new_graph[node] = []
    return new_graph

def read_file(file_path):
    """
    Read the file and generate the graph.
    """
    '''    graph = {}
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
            if len(line) == 1:
                graph[int(line[0])] = []
            for node in line:
                try:
                    graph[int(line[0])].append(int(node))
                except KeyError:
                    if node is not line[0]:
                        graph.update({int(line[0]):[int(node)]})'''
    graph = {}
    with open(file_path) as f:
        nos = [x.strip().split() for x in f.read().replace('(',' ').replace(')',' ').strip().split('\n')][1:]
    for no in nos:
        graph[int(no[0])] = [int(x) for x in no[1:]]
    return graph

def part_1(graph):
    nodes = list(graph.keys())
    reverse = reverse_graph(graph, nodes)
    print('Components:')
    components = scc(graph, reverse, nodes)
    for component in components:
        print(components[component])
    print()
    return components, nodes

def part_2(graph):
    sorting = dfs_topsort(graph)
    print('DFS Topological sorting:')
    print(sorting)

def dfs_topsort(graph):         # recursive dfs with
    L = []                      # additional list for order of nodes
    color = {u : "white" for u in graph}
    for u in graph:
        if color[u] == "white":
            dfs_visit(graph, u, color, L)
    L.reverse()                  # reverse the list
    return L                     # L contains the topological sort

def dfs_visit(graph, u, color, L):
    color[u] = "gray"
    for v in graph[u]:
        if color[v] == "white":
            dfs_visit(graph, v, color, L)
    color[u] = "black"      # when we're done with u,
    L.append(u)             # add u to list (reverse it later!)

def main(filename):
    graph = read_file(filename)
    comp, nodes = part_1(graph)
    if len(comp) == len(nodes):
        part_2(graph)
    else:
        print("ERROR: Cyclic graph!")

if __name__ == '__main__':
    PRS = argparse.ArgumentParser(description='Trabalho de Grafos 2016/2'
                                  + '\n\tArthur Zachow Coelho'
                                  + '\n\tFelipe de Almeida Graeff'
                                  + '\n\tHenrique Barboza',
                                  epilog="Sources:"
                                  + "\nhttps://en.wikipedia.org/wiki/Strongly_connected_component"
                                  + "\nhttps://www.ime.usp.br/~pf/algoritmos_para_grafos_OLD/aulas/strong-comps.html"
                                  + "\nhttps://teacode.wordpress.com/2013/07/27/algo-week-4-graph-search-and-kosaraju-ssc-finder/"
                                  + "\nhttps://gist.github.com/JeremieGomez/74de2d3e1268c48e63a3"
                                  + "\nhttps://algocoding.wordpress.com/2015/04/05/topological-sorting-python/"
                                  + "\nhttp://www.cse.cuhk.edu.hk/~taoyf/course/2100sum11/lec14.pdf"
                                  + "\nhttps://www.cs.usfca.edu/~galles/visualization/TopoSortDFS.html"
                                  + "\nhttps://en.wikipedia.org/wiki/Topological_sorting"
                                  + "\nhttp://www.geeksforgeeks.org/topological-sorting/",
                                  formatter_class=argparse.RawTextHelpFormatter)
    PRS.add_argument('-f', dest='file', required=True, help='Path to the graph file.')
    ARGS = PRS.parse_args()
    FILENAME = ARGS.file
    main(FILENAME)
