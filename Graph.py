class DirGraph(dict): # Undirected graph¡
  
  def addVert(s, a):
      s[a] = []

  def add(s, a, b):
    if not a in s:
      s.addVert(a)
    if not b in s[a]:
      s[a].append(b)

  def remove(s, a, b):
    s[a].remove(b)

class UndirGraph(DirGraph):

  def add(s, a, b):
    DirGraph.add(s, a, b)
    DirGraph.add(s, b, a)

  def remove(s, a, b):
    DirGraph.remove(s, a, b)
    DirGraph.remove(s, b, a)

  def colorMap(s): # greedy algorithm
    maxColor = 0
    coloring = {}
    for v in list(s.keys()):
      color = 1
      takenColors = (coloring[i] for i in s[v] if i in coloring) #this is an iterable but not a list
      while color in takenColors:
        color += 1
      coloring[v] = color
      if color > maxColor:
        maxColor = color
    return coloring, maxColor
      
  
class NotSelfGraph(UndirGraph):
  def add(s, a, b):
    if a != b:
      UndirGraph.add(s, a, b)
