import random, math, os, numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2 # pip install opencv-python

from regionGrower import regionGrower
from perlinNice import *

testsFolder = "tests"

def generateMap(size, name):
  name = os.path.join(testsFolder,name)

  print(name, "start")

  arr = perlinNoiseFreq(size, [(2,1),(6, 0.5), (20, 0.2)])
  #arr = perlinNoiseFreq(size, [(2,2),(5,1)])
  img.imsave(f'{name}_0perlinNoise.png', arr)
  print("  perlin hecho")

  # _, arr = cv.threshold(arr, 0.04, 1, cv.THRESH_TOZERO)
  # # arr, treshold, maxvalue, type
  # img.imsave(f'{name}/2umbralizado.png', arr)

  arr = np.array(256*arr, dtype = 'uint8')
  arr = cv2.medianBlur(arr, 3)
  img.imsave(f'{name}_1filtroMediana.png', arr)
  print("  mediana hecho")

  arr = regionGrower(arr,10,threshold=20, thresholdGrowth=1.1)
  img.imsave(f'{name}_2regionGrower.png', arr)

  print("  terminado")

if not os.path.exists(testsFolder):
    os.makedirs(testsFolder)

for i in range(10):
  generateMap(100, str(i))