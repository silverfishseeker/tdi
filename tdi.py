import random, math, os, shutil, numpy as np
import matplotlib.image as img
import cv2 # pip install opencv-python

from regionGrower import regionGrower
from perlinNice import *

testsFolder = "tests"
def generateMap(name, size, contryNumber, perlin, threshold, thresholdGrowth, seeLevel,decreaseFactor, minEarthSize, medianSize, seeMedianSize):
  
  class Img():
    def __init__(s):
      s.n=0
    def print(s,arr, subName):
      img.imsave(f'{name}_{s.n}{subName}.png', cv2.resize(arr, dsize=(2000, 2000), interpolation=cv2.INTER_NEAREST))
      s.n+=1
  im = Img()

  name = os.path.join(testsFolder,name)

  perlin = perlinNoise(size, perlin)*256
  im.print(perlin, "perlinNoise")

  # See
  seeMedianSize = size//seeMedianSize
  seeMedianSize = seeMedianSize+seeMedianSize%2+1 # tiene que ser impar
  maxSee = size*size - int(size*size*minEarthSize)
  currRange = 256
  while True:
    see = cv2.GaussianBlur(perlin.astype("uint8"), (seeMedianSize,seeMedianSize), cv2.BORDER_DEFAULT)
    _, see = cv2.threshold(see, seeLevel, 255, cv2.THRESH_BINARY)
    zeroPixels = size*size - cv2.countNonZero(see)
    if zeroPixels < maxSee:
      break
    currRange*=decreaseFactor
    perlin= perlin*decreaseFactor+256-currRange
    im.print(see, "seeTry")
  im.print(see, "seeGaussianYUmbralizado")

  see = cv2.medianBlur(see, seeMedianSize)
  im.print(see, "seeMediana")


  arr = regionGrower(perlin, contryNumber, see, zeroPixels, threshold, thresholdGrowth)
  im.print(arr, "regionGrower")

  medianSize = size//medianSize
  medianSize = medianSize+medianSize%2+1
  arr = cv2.medianBlur(arr, medianSize)
  im.print(arr, "filtroMediana")

  print(name,"terminado")
  print()

if __name__ == "__main__":


  if os.path.exists("x"):
    shutil.rmtree("x")
  os.makedirs("x")


  if os.path.exists(testsFolder):
    shutil.rmtree(testsFolder)
  os.makedirs(testsFolder)
  for i in range(1000):
    generateMap(str(i),
      size=20,
      contryNumber=3,
      #perlin=[(2, 2), (5,1), (10, 1), (20, 0.2), (30, 0.1), (100, 0.2)],
      perlin=[(2, 1)],
      threshold=1,
      thresholdGrowth=1.5,
      seeLevel=130,
      decreaseFactor=0.9,
      minEarthSize=0.4, #si es muy bajo puede que no termine por no enconrar huecos libres para semillas
      medianSize=100,
      seeMedianSize=10)
  
  print("END")