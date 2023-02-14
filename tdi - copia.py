import numpy as np
import matplotlib.pyplot as plt
# from perlin_noise import PerlinNoise

# https://github.com/pvigier/perlin-numpy
from perlin_numpy import generate_fractal_noise_2d

# import random

# def compoundNoise(octaves, weights, xpic, ypic, seed=int(random.random()*1000000000)):
#   sumW= sum(i for i in weights)
#   noises = [PerlinNoise(i, seed) for i in octaves]

#   return [[
#     sum(noises[k]([i/xpic, j/ypic])*weights[k] for k in range(len(noises)))/sumW
#     for j in range(ypic)] for i in range(xpic)]
  
# noise = PerlinNoise(10,1)
# xpix, ypix = 100, 100

# pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
# plt.imshow(pic, cmap='gray')
# plt.show()

# noises = compoundNoise([4,10,40,80], [50,20,2,4], 100, 100)
# plt.imshow(noises, cmap='gray')
# plt.show()

noises = generate_fractal_noise_2d((1024, 1024), (2,2), 10, 0.4)
plt.imshow(noises, cmap='gray')
plt.show()




# pic2 = [noise (i/xpix) for i in range(xpix)]
# plt.plot(pic2)
# plt.show()

def randomRegionGrower(arr, seedBag, seed=random.random()):
  
  random.seed(seed)
  xlen = len(arr)
  ylen = len(arr[0])
  coord2id = np.zeros((xlen, ylen), np.int16)
  id2coord = []
  id2coordEdge = [None]
  openedRegions = []

  rdIndex = lambda len: int(random.random()*len)
  isfree = lambda x, y: x >= 0 and y >= 0 and x < xlen and y < ylen and coord2id[x][y] == 0

  def addEdge(x, y, region):
      for i, j in [(0,1),(0,-1),(1,0),(-1,0)]:
        x2, y2 = x+i, y+j
        if isfree(x,y):
          id2coordEdge[region].append((x2, y2))
     
  for i in range(1, seedBag+1):
    x = rdIndex(xlen)
    y = rdIndex(ylen)
    if isfree(x, y):
      id2coord.append([(x,y)])
      id2coordEdge.append([])
      addEdge(x, y, i)
      openedRegions.append(i)

  while openedRegions:
    region = openedRegions[rdIndex(len(openedRegions))]
    if not id2coordEdge[region]:
      openedRegions.remove(region)
    else:
      x, y = id2coordEdge[region].pop(rdIndex(len(id2coordEdge[region])))
      if coord2id[x][y] != 0:
        coord2id[x][y] = region
        id2coord[region].append((x,y))
        addEdge(x, y, i)

  return coord2id
