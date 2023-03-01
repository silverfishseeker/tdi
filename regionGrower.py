import random, numpy as np
import matplotlib.image as img, cv2
from alive_progress import alive_bar

class Img():
  n=0
  def print(arr):
    arr = cv2.resize(arr, dsize=(1200, 1200), interpolation=cv2.INTER_NEAREST)
    img.imsave(f'x/{Img.n}.png', arr)
    Img.n+=1

def regionGrower(image, nregions, mask, zeroPixels, threshold, thresholdGrowth=1.1):

  class Counter(): #para tener referencia a un número
    def start(init):
      Counter.n = init
    
  def isFreePixel(arr, point):
    if point[0]<0 or point[1]<0: # indeces negativos son válidos en python
      return False
    try:
      return mask[point] and arr[point] == 0
    except IndexError:
      return False

  class Region():
    def __init__(s, seed, value, freespace):
      s.free = freespace # pixeles disponibles
      s.val = value # identificador
      s.border = []
      s.seed = seed
      s.center = s.seed
      s.size = 0
      if s.isfree(seed):
        s.addPoint(seed)
      else:
        raise ValueError("el seed no está disponible")

    def isfree(s, point):
      return isFreePixel(s.free, point)

    def addPoint(s, point):
      s.free[point] = s.val
      Counter.n-=1
      x, y = point
      for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
        new = x+i, y+j
        if s.isfree(new) and new not in s.border:
          s.border.append(new)

      #dintance
      s.size +=1
      s.center = (s.center[0]+point[0], s.center[1]+point[1])
      bar()
      # Img.print(s.free)
      # img.imsave("xxx.png",cv2.resize((mask.astype("bool") & ~s.free.astype("bool")).astype("uint8"), dsize=(2000, 2000), interpolation=cv2.INTER_NEAREST))
    
    def grow(s):
      checkedBorder = []
      while s.border:
        # punto aleatorio en la frontera:
        candidate = s.border.pop(int(random.random()*len(s.border)))
        if s.isfree(candidate):
          # manhattan con el punto medio:
          distance = abs(s.center[0] / s.size - candidate[0]) + abs(s.center[1] / s.size - candidate[1])
          # comparamos nivel de gris y multiplicamos por la distancia :
          if abs(int(image[seed]) - int(image[candidate]))*distance < threshold:
            s.addPoint(candidate)
          else:
            checkedBorder.append(candidate)
      # guardamos los puntos que no han pasado el threshold para cuando este suba:
      s.border = checkedBorder
    
  xlen, ylen = image.shape
  freespace = np.zeros((xlen, ylen)) # píxeles sin escoger
  Counter.start(xlen*ylen-zeroPixels)
  regions = []
  closed = []
  regionVal = 1
  actualNRegions = 0

  # grow until the end
  with alive_bar(Counter.n) as bar:
    while Counter.n > 0:
      if not regions:
        if closed:
          regions = closed
          closed = []
          threshold*=thresholdGrowth
        else:
          while regionVal < nregions+1 or not (regions or closed):
            loop = True
            while loop:
              seed = int(random.random()*xlen), int(random.random()*ylen)
              if isFreePixel(freespace,seed):
                loop = False
                r = Region(seed, regionVal, freespace)
                regions.append(r)
                r.grow()
                regionVal+=1
                actualNRegions+=1

      curr = regions.pop()
      curr.grow()
      if curr.border:
        closed.append(curr)
      #print(Counter.n, cv2.countNonZero(freespace), sum(x.size for x in discarded), threshold)
    
  return (freespace * 256 / (actualNRegions+1)).astype("uint8")
