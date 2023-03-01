import random, math, os, shutil, numpy as np
import matplotlib.image as img
import cv2 # pip install opencv-python
from regionGrower import regionGrower
from perlinNice import perlinNoise
#from decimal import * # me ha pasado un poco con el tamaño de los numbers

testsFolder = "tests"


class Img():
  def __init__(s, name):
    s.n=0
    s.name = name
  def print(s,arr, subName):
    img.imsave(f'{s.name}_{s.n}{subName}.png', cv2.resize(arr, dsize=(2000, 2000), interpolation=cv2.INTER_NEAREST))
    s.n+=1

def generateMap(name, size, contryNumber, perlinRegions, perlinSee, threshold, thresholdGrowth, distanceFactor, seeLevel,decreaseFactor, minEarthSize, medianSize, seeMedianSize):
  
  im = Img(os.path.join(testsFolder,name))

  print(name, "comienza")
  seeperlin = perlinNoise(size, perlinSee)*256
  im.print(seeperlin, "perlinSee")

  # See
  seeMedianSize = size//seeMedianSize
  seeMedianSize = seeMedianSize+seeMedianSize%2+1 # tiene que ser impar
  maxSee = size*size - int(size*size*minEarthSize)
  currRange = 256
  while True: # bajamos el agua hasta que haya suficiente tierra
    see = cv2.GaussianBlur(seeperlin.astype("uint8"), (seeMedianSize,seeMedianSize), cv2.BORDER_DEFAULT)
    _, see = cv2.threshold(see, seeLevel, 255, cv2.THRESH_BINARY)
    zeroPixels = size*size - cv2.countNonZero(see)
    if zeroPixels < maxSee:
      break
    newRange = currRange*decreaseFactor
    seeperlin= seeperlin*decreaseFactor+currRange-newRange
    currRange=newRange
    im.print(see, "seeTry")

  im.print(see, "seeGaussianYUmbralizado")

  see = cv2.medianBlur(see, seeMedianSize)
  im.print(see, "seeMediana")

  # regions
  arr = perlinNoise(size, perlinRegions)*256
  im.print(arr, "perlinNoise")

  arr = regionGrower(arr, contryNumber, see, zeroPixels, threshold, thresholdGrowth, distanceFactor)
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
      size=1000,
      contryNumber=20,
      perlinRegions=[(2, 0.2), (5,0.2), (10, 0.5), (20, 1), (30, 1), (100, 0.1)],
      perlinSee=[(2, 2), (5,1), (10, 1), (20, 0.5), (30, 0.1), (100, 0.1)],
      #perlin=[(2, 1)],
      threshold=100,
      thresholdGrowth=1.5,
      distanceFactor = lambda x: x**2,
      seeLevel=130,
      decreaseFactor=0.9, # en el rango (0,1)
      minEarthSize=0.4, #si es muy bajo puede que no termine por no enconrar huecos libres para semillas
      medianSize=100, # dividir la imagen en este número de partes para calcular el tamaño de la mediana
      seeMedianSize=50)
  
  print("END")