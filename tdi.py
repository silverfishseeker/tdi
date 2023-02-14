import random, math, os, numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2 as cv # pip install opencv-python
# https://github.com/pvigier/perlin-numpy
from perlin_numpy import generate_fractal_noise_2d # pip3 install git+https://github.com/pvigier/perlin-numpy

def regionGrower(image, nregions, threshold, seed=random.random()):

  def judge(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(image[p1] - image[p2]) < threshold

  class Region():
    def isfree(s, point):
      if point[0]<0 or point[1]<0:
        return False
      try:
        return s.free[point] == 0
      except IndexError:
        return False

    def addPoint(s, point):
      x, y = point
      s.place.append((x,y))
      for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
        new = x+i, y+j
        if s.isfree(new) and judge((x,y), new):
          s.border.append(new)

    def __init__(s, seed, value, freespace):
      s.free = freespace
      s.val = value
      s.place = []
      s.border = []
      s.seed = seed
      if s.isfree(seed):
        s.addPoint(seed)

    def __str__(s):
      return str(s.val)+"|"+str(s.seed)

    def grow(s):
      while s.border:
        candidate = s.border.pop(int(random.random()*len(s.border)))
        if s.isfree(candidate):
          s.addPoint(seed)
          s.free[candidate] = s.val
          return True
      return False

  random.seed(seed)
  xlen, ylen = image.shape

  freespace = np.zeros((xlen, ylen))
  regions = []
  closed = []
  freenumber = xlen*ylen

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
      threshold*=1.1

    curr = regions.pop(0)
    if (curr.grow()):
      regions.append(curr)
      freenumber += -1
    else:
      closed.append(curr)

  return freespace * 256 / nregions

testsDir = "tests"
def generateMap(size, name):
  try:
    os.mkdir(os.path.join(testsDir,name))
  except FileExistsError:
    pass

  print("start")
  arr = generate_fractal_noise_2d((size, size), (2,2), int(math.log(size,10)), 0.4)
  # shape(alto, ancho),
  # res(number of peridos per axis),
  # octaves: number of octaves,
  # persistence:scaling factor between octaves
  # lacunarity=2 : The frequency factor between two octaves
  # shape must be a multiple of (lacunarity**(octaves-1)*res)
  img.imsave(f'{name}/0perlinNoise.png', arr)

  # we get it positive
  arr = arr **2
  img.imsave(f'{name}/1square.png', arr)

  # mini, maxi = 0,0
  # for k in arr:
  #   for j in k:
  #     if j < mini:
  #       mini = j
  #     if j > maxi:
  #       maxi = j
  # print(mini, maxi)

  _, arr = cv.threshold(arr, 0.04, 1, cv.THRESH_TOZERO)
  # arr, treshold, maxvalue, type
  img.imsave(f'{name}/2umbralizado.png', arr)

  arr = ndimage.median_filter(arr, size=size//20)
  # arr, size
  img.imsave(f'{name}/3filtroMediana.png', arr)

  print(name, "terminado")

for i in range(10):
  generateMap(1024, str(i))


# arr = regionGrower(np.zeros((10,10)), 10, 1)
# img.imsave("prueba.png", arr)