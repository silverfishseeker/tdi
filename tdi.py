import random, math, os, numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2 as cv # pip install opencv-python

from regionGrower import regionGrower
from perlinNice import *

def generateMap(size, name):
  name = os.path.join("tests",name)
  try:
    os.mkdir(name)
  except FileExistsError:
    pass

  print("start")

  #arr = np.asarray( perlinNoise(size, size, [200,100,30,8],[50,30,19,1]))
  #arr = np.asarray( perlinNoise(size, size, [(200,50),(100,30),(30,19),(8,1)]))
  arr = perlinNoiseFreq(size, [(2,0.5),(6, 0.3), (20, 0.2)])

  img.imsave(f'{name}/0perlinNoise.png', arr)

  # _, arr = cv.threshold(arr, 0.04, 1, cv.THRESH_TOZERO)
  # # arr, treshold, maxvalue, type
  # img.imsave(f'{name}/2umbralizado.png', arr)

  # arr = ndimage.median_filter(arr, size=size//20)
  # # arr, size
  # img.imsave(f'{name}/3filtroMediana.png', arr)

  arr = regionGrower(arr,10,1)
  img.imsave(f'{name}/4regionGrower.png', arr)

  print(name, "terminado")

for i in range(1):
  generateMap(1024, str(i))