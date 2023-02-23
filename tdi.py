import random, math, os, shutil, numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
from scipy import ndimage
import cv2 # pip install opencv-python

from regionGrower import regionGrower
from perlinNice import *

testsFolder = "tests"

def generateMap(size, name, perlinContry, perlinSee, threshold, thresholdGrowth, seeLevel, medianSize, seeMedianSize):
  name = os.path.join(testsFolder,name)

  #arr = perlinNoiseFreq(size, [(2,2),(5,1)])
  perlin = perlinNoise(size, perlinContry)
  perlin = np.array(256*perlin, dtype = 'uint8') #pasamos de [0,1) a [0,255]
  img.imsave(f'{name}_0perlinNoise.png', perlin)

  arr = regionGrower(perlin,10,threshold, thresholdGrowth)
  img.imsave(f'{name}_1regionGrower.png', arr)

  medianSize = size//medianSize
  medianSize = medianSize+medianSize%2+1
  arr = cv2.medianBlur(arr, medianSize)
  img.imsave(f'{name}_2filtroMediana.png', arr)


  # see = perlinNoise(size, perlinSee)
  # see = np.array(256*see, dtype = 'uint8') #pasamos de [0,1) a [0,255]
  # img.imsave(f'{name}_5see.png', see)

  
  seeMedianSize = size//seeMedianSize
  seeMedianSize = seeMedianSize+seeMedianSize%2+1

  see = cv2.GaussianBlur(perlin, (seeMedianSize,seeMedianSize), cv2.BORDER_DEFAULT)
  img.imsave(f'{name}_5seeGaussianBlur.png', see)

  _, see = cv2.threshold(see, seeLevel, 256, cv2.THRESH_BINARY_INV)
  img.imsave(f'{name}_6seeUmbralizado.png', see)

  see = cv2.medianBlur(see, seeMedianSize)
  img.imsave(f'{name}_7seeMediana.png', see)


  arr = arr*see
  img.imsave(f'{name}_8mareNostrum.png', arr)
  print(name,"terminado")

if __name__ == "__main__":
  if os.path.exists(testsFolder):
    shutil.rmtree(testsFolder)
  os.makedirs(testsFolder)
  for i in range(10):
    generateMap(200, str(i),
      perlinContry=[(10, 1), (20, 0.2), (100, 0.2)],
      perlinSee=[(2, 2), (5,1),(10, 1), (30, 0.05)],
      threshold=1,
      thresholdGrowth=1.1,
      seeLevel=130,
      medianSize=100,
      seeMedianSize=10)