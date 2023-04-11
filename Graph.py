class Graph(set): # Undirected graph¡
  def add(s, a, b):
    set.add(s, (a,b) if a < b else (b,a))

  def __contains__(s, key):
    a,b = key
    return set.__contains__(s,(a,b)) or set.__contains__(s,(b,a))

  def remove(s, a, b):
    try:
      return set.remove(s,(b,a))
    except KeyError:
      return set.remove(s,(a,b)) # si no está ninguno lanzamos KeyError de set
  
class NotSelfGraph(Graph):
  def add(s, a, b):
    if a != b:
      Graph.add(s, a, b)
