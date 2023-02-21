import random, math, os, shutil, numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2 # pip install opencv-python

from regionGrower import regionGrower
from perlinNice import *

testsFolder = "tests"

def generateMap(size, name):
  name = os.path.join(testsFolder,name)

  #arr = perlinNoiseFreq(size, [(2,2),(5,1)])
  arr = perlinNoise(size, [(2,1),(6, 0.5), (10, 0.2)])
  arr = np.array(256*arr, dtype = 'uint8') #pasamos de [0,1) a [0,255]
  img.imsave(f'{name}_0perlinNoise.png', arr)

  # _, arr = cv2.threshold(arr, 100, 256, cv2.THRESH_TOZERO)
  # # arr, treshold, maxvalue, type
  # img.imsave(f'{name}_1umbralizado.png', arr)

  arr = regionGrower(arr,10,threshold=1, thresholdGrowth=1.1)
  img.imsave(f'{name}_2regionGrower.png', arr)

  medianSize = size//100
  medianSize = medianSize+medianSize%2+1
  arr = cv2.medianBlur(arr, medianSize)
  img.imsave(f'{name}_3filtroMediana.png', arr)

  print(name,"terminado")

if __name__ == "__main__":
  shutil.rmtree(testsFolder)
  os.makedirs(testsFolder)
  for i in range(10):
    generateMap(200, str(i))