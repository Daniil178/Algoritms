from random import randint
import pickle

n = randint(10, 50)
graph = {}
size = 0
while size < n:
  vertex = size + 1
  if not vertex in graph:
    graph[vertex] = []
    size += 1
edge = randint(size// 2, (size // 2) * (size - 1))
k = 0
while k < edge:
  v1 = randint(1, size)
  v2 = randint(1, size)
  if v2 in graph and v1 in graph and not v2 in graph[v1]:
    if v1 != v2:
      graph[v1].append(v2), graph[v2].append(v1)
      k += 1 

with open("out_graph", "wb") as out:
  pickle.dump(graph, out)

print(f"size graph - {size}, edges number - {edge}")

for i in list(dict.items(graph)):
  print(i[0], '-', *i[1], sep=' ')
