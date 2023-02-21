import random, numpy as np

def regionGrower(image, nregions, threshold=0.1, thresholdGrowth=1.1):

  def isFreePixel(arr, point):
    if point[0]<0 or point[1]<0: # indeces negativos son válidos en python
      return False
    try:
      return arr[point] == 0
    except IndexError:
      return False

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
      return isFreePixel(s.free, point)

    def judge(s,point):
      return abs(int(image[seed]) - int(image[point])) < threshold

    def addPoint(s, point):
      s.place.append(point)
      s.free[point] = s.val
      x, y = point
      for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
        new = x+i, y+j
        if s.isfree(new):
          s.border.append(new)

    def __str__(s):
      return str(s.val)+"|"+str(s.seed)

    def grow(s):
      checkedBorder = []
      while s.border:
        candidate = s.border.pop(int(random.random()*len(s.border)))
        if s.isfree(candidate) and s.judge(candidate):
          s.addPoint(candidate)
          s.border.extend(checkedBorder)
          return True
        else:
          checkedBorder.append(candidate)
      s.border.extend(checkedBorder)
      return False
    
    def spread(s):
      gained = 0
      while s.grow():
        gained+=1
      return gained

  xlen, ylen = image.shape

  freespace = np.zeros((xlen, ylen),dtype=int) # píxeles sin escoger
  regions = []
  freenumber = xlen*ylen-nregions

  #seeding and first grow
  for i in range(nregions):
    while(freenumber > 0):
      seed = int(random.random()*xlen), int(random.random()*ylen)
      if isFreePixel(freespace,seed):
        r = Region(seed, i+1, freespace)
        freenumber-= 1 + r.spread()
        regions.append(r)
        break

  # grow until the end
  closed = []
  while freenumber > 0:
    if len(regions) == 0:
      regions = closed
      closed = []
      threshold*=thresholdGrowth

    curr = regions.pop()
    freenumber -= curr.spread()
    closed.append(curr)
    #print(freenumber, threshold, len(closed), curr.val)

  return freespace * 256 / nregions
