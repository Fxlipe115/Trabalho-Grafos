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

    def __repr__(self):
        """
        __repr__ method override.
        """
        return repr(str(self.start) + '-' + str(self.end))


def read_file(file_path):
    nodes = []
    edges = []
    for line in open(file_path):
        try:
            if int(line):
                line = ''
        except:
            pass
        line = line.replace(")",'')
        line = line.replace("(",'')
        line = line.split()
        if line:
            nodes.append(Node(line[0]))
            for node in line:
                if node is not line[0]:
                    edges.append(Edge(line[0],node))

    return nodes,edges

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None

if __name__ == '__main__':
    filename = input()
    nodes, edges = read_file(filename)
    graph = (nodes, edges)
    print(graph)
