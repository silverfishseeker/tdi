import random, numpy as np

def regionGrower(image, nregions, threshold=1, thresholdGrowth=1.1):

  def judge(p1, p2):
    return abs(image[p1] - image[p2]) < threshold

  class Region():
    def __init__(s, seed, value, freespace):
      s.free = freespace # pixeles disponibles
      s.val = value # identificador
      s.place = []
      s.border = []
      s.seed = seed
      if s.isfree(seed):
        s.addPoint(seed)
      else:
        raise ValueError

    def isfree(s, point):
      if point[0]<0 or point[1]<0: # indeces negativos son válidos en python
        return False
      try:
        return s.free[point] == 0
      except IndexError:
        return False

    def addPoint(s, point):
      s.place.append(point)
      s.free[point] = s.val
      x, y = point
      for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
        new = x+i, y+j
        if s.isfree(new) and judge((x,y), new):
          s.border.append(new)

    def __str__(s):
      return str(s.val)+"|"+str(s.seed)

    def grow(s):
      while s.border:
        candidate = s.border.pop(int(random.random()*len(s.border)))
        if s.isfree(candidate):
          s.addPoint(candidate)
          return True
      return False

  xlen, ylen = image.shape

  freespace = np.zeros((xlen, ylen),dtype=int) # píxeles sin escoger
  regions = []
  closed = []
  freenumber = xlen*ylen-nregions

  for i in range(nregions):
    while(True):
      seed = int(random.random()*xlen), int(random.random()*ylen)
      for r in regions:
        if r.seed == seed:
          break
      else:
        regions.append(Region(seed, i+1, freespace))
        break

  while freenumber > 0:
    if len(regions) == 0:
      regions = closed
      closed = []
      threshold*=thresholdGrowth

    curr = regions.pop(0)
    if (curr.grow()):
      regions.append(curr)
      freenumber += -1
    else:
      closed.append(curr)

  return freespace * 256 / nregions
