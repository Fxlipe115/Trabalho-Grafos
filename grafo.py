grafo_teste = {'0' : ['1'],
		 '1' : ['4'],
		 '2' : ['5'],
		 '3' : ['1'],
		 '4' : ['3', '5'],
		 '5' : ['2']}
		 
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