import random, numpy as np
import matplotlib.image as img, cv2
import bisect
from alive_progress import alive_bar

class Img():
  n=0
  def print(arr):
    arr = cv2.resize(arr, dsize=(1200, 1200), interpolation=cv2.INTER_NEAREST)
    img.imsave(f'{Img.stepsFolder}/{Img.n}.png', arr)
    Img.n+=1


class Counter(): #para tener referencia a un número
  def start(init):
    Counter.n = init


class Region():
  def staticInit(image, lienzo, pixelsDict, mask, threshold, distanceFactor, thresholdGrowth, condition, randomDistr, isPrint):
    Region.image = image
    Region.lienzo = lienzo # pixeles disponibles
    Region.pixelsDict = pixelsDict
    Region.mask = mask
    Region.threshold = threshold
    Region.distanceFactor = distanceFactor
    Region.thresholdGrowth = thresholdGrowth
    Region.condition = condition
    Region.randomDistr = randomDistr
    Region.isPrint = isPrint

  def isfree(point):
    if point[0]<0 or point[1]<0: # indeces negativos son válidos en python
      return False
    try:
      return Region.mask[point] and Region.lienzo[point] == 0
    except IndexError:
      return False

  def __init__(s, seed, value):
    s.val = value # identificador
    s.border = []
    s.seed = seed
    s.center = s.seed
    s.size = 0
    if Region.isfree(seed):
      s.addPoint(0,seed)
    else:
      raise ValueError("el seed no está disponible")

  def __lt__(s, other):
    return type(other) is Region and s.size < other.size
  
  # def __eq__(s, other):
  #   return type(other) is Region and s.size == other.size
  
  def addPoint(s, dist, point):
    Region.lienzo[point] = s.val
    Region.pixelsDict[s.val] = point
    Counter.n-=1
    x, y = point
    for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
      new = x+i, y+j
      if Region.isfree(new):
        bisect.insort(s.border, (dist+1, new))

    #Img.print(Region.lienzo)

    #dintance
    s.size +=1
    s.center = (s.center[0]+point[0], s.center[1]+point[1])
  
  def grow(s):
    checkedBorder = []
    hasGrown = False
    while s.border:
      # punto aleatorio en la frontera:
      dist, candidate = s.border.pop(
        int(Region.randomDistr(random.random()) * len(s.border))
      )

      if Region.isfree(candidate):
        
        #### NOS LA METEMOS O NO NOS LA METEMOS ####
        if Region.condition(Region.image[candidate], Region.distanceFactor(dist), Region.threshold):
          s.addPoint(dist, candidate)
          hasGrown = True
        else:
          bisect.insort(checkedBorder, (dist, candidate))

    # guardamos los puntos que no han pasado el threshold para cuando este suba:
    s.border = checkedBorder

    if Region.isPrint and hasGrown:
      Img.print(Region.lienzo)
  

def regionGrower(image, nregions, mask, zeroPixels, threshold, thresholdGrowth, distanceFactor,stepsFolder,maxSeedTries, condition, randomDistr,isPrint):
  xlen, ylen = image.shape
  lienzo = np.zeros((xlen, ylen)) # píxeles sin escoger
  Counter.start(xlen*ylen-zeroPixels)
  Img.stepsFolder = stepsFolder
  regions = []
  closed = []
  regionVal = 1
  actualNRegions = 0
  prevCunterN = Counter.n # para la barra chula de progreso
  pixelsDict = {}
  Region.staticInit(image, lienzo, pixelsDict, mask, threshold, distanceFactor,thresholdGrowth, condition, randomDistr, isPrint)

  # grow until the end
  with alive_bar(Counter.n) as bar:
    while Counter.n > 0:
      if not regions:
        if closed:
          regions = closed
          closed = []
          Region.threshold=Region.thresholdGrowth(Region.threshold)
        else:
          while regionVal < nregions+1 or not (regions or closed):
            for _ in range(maxSeedTries):
              seed = int(random.random()*xlen), int(random.random()*ylen)
              if Region.isfree(seed) and Region.image[seed] < Region.threshold:
                r = Region(seed, regionVal)
                regions.append(r)
                r.grow()
                regionVal+=1
                actualNRegions+=1
                break
            else:
              Region.threshold=Region.thresholdGrowth(Region.threshold)

      curr = regions.pop()
      curr.grow()
      if curr.border:
        closed.append(curr)

      bar(prevCunterN-Counter.n)
      prevCunterN = Counter.n
      #print(Counter.n, cv2.countNonZero(freespace), sum(x.size for x in discarded), threshold)
    
  return (lienzo * 256 / (actualNRegions+1)).astype("uint8")
