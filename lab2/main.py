import pickle
import sys

def check_euler(graph):
  for i in list(dict.keys(graph)):
      if len(graph[i]) % 2 == 1:
        return False
  return True

def find_euler_path(graph):
  if check_euler(graph) == False:
    return []
  else:
    S = [] #stack
    path = []
    v = 1
    S.append(v)
    while len(S) > 0:
      w = S[-1]
      if len(graph[w]) == 0:
        path.append(w)
        S = S[:-1]
      else:
        edge = graph[w][-1]
        graph[w] = graph[w][:-1]
        graph[edge] = graph[edge][:graph[edge].index(w)] + graph[edge][graph[edge].index(w) + 1:]
        S.append(edge)
    return path

def hamilton(curr, Visited, Path, graph):    
    node_curr = list(graph.keys())[curr]
    Path.append(node_curr)
    n = len(list(dict.keys(graph)))
    if len(Path) == n:
        if Path[-1] in graph[Path[0]]:
            return True
        else:
            Path.pop()
            return False
    Visited[curr] = True
    for next in range(n):
        node_next = list(dict.keys(graph))[next]
        if node_next in graph[node_curr] and not Visited[next]:
            if hamilton(next, Visited, Path, graph):
                return True
    Visited[curr] = False
    Path.pop()
    return False

def find_ham_path(graph):
    n = len(list(dict.keys(graph)))
    visited = [False] * n
    path = []
    for i in range(1, n): 
        if len(graph[i]) <= 1:
            return path
    find = hamilton(1, visited, path, graph)
    if find == True:
        path = path + [path[0]]
    else:
        path = []
    return path

if __name__ == "__main__":
	filename = "out_graph" 
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	
	try:
		with open(filename, "rb") as inp:
  			graph = pickle.load(inp)
		path = find_ham_path(graph)
		if path == []:
                	print("Graph isn`t Hamilton`s")
		else:
			print("Graph is Hamilton`s")
			print(*path)
		
		path = find_euler_path(graph)
		if len(path) != 0:
  			print("Graph is euler")
  			print(*path)
		else:
    			print("Graph hasn`t euler cycle")
	except FileNotFoundError:
		print("Error, this file don`t exist")
