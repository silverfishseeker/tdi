import random, math, os, shutil, numpy as np
import matplotlib.image as img
import cv2 # pip install opencv-python
from regionGrower import regionGrower
from perlinNice import perlinNoise
#from decimal import * # me ha pasado un poco con el tamaño de los numbers

testsFolder = "tests"
stepsFolder = "steps"


class Img():
  def __init__(s, name):
    s.n=0
    s.name = name
  def print(s,arr, subName):
    img.imsave(f'{s.name}_{s.n}{subName}.png', cv2.resize(arr, dsize=(2000, 2000), interpolation=cv2.INTER_NEAREST))
    s.n+=1

def generateMap(name, size, contryNumber, perlinRegions, perlinSee, threshold, thresholdGrowth, distanceFactor, seeLevel,decreaseFactor, minEarthSize, medianSize, maxSeedTries, condition):
  
  im = Img(os.path.join(testsFolder,name))

  medianSize = size//medianSize
  medianSize = medianSize+medianSize%2+1 # tiene que ser impar

  # See
  print(name, "comienza")
  seePerlin = (perlinNoise(size, perlinSee)*256).astype("uint8")
  im.print(seePerlin, "perlinSee")

  minSee = size*size - int(size*size*minEarthSize)
  while True: # bajamos el agua hasta que haya suficiente tierra
    #see = cv2.GaussianBlur(seeperlin.astype("uint8"), (seeMedianSize,seeMedianSize), cv2.BORDER_DEFAULT)
    _, see = cv2.threshold(seePerlin, seeLevel, 255, cv2.THRESH_BINARY)
    if size*size - cv2.countNonZero(see) < minSee:
      break
    seeLevel*=decreaseFactor
    im.print(see, "seeTry")

  im.print(see, "seeUmbralizado")

  # see = cv2.medianBlur(see, seeMedianSize)
  # im.print(see, "seeMediana")
  
  kernel = np.ones((medianSize, medianSize), np.uint8)
  radius = medianSize//2
  for i in range(medianSize):
    for j in range(medianSize):
      if ((i-radius)**2+(j-radius)**2)**0.5 > radius:
        kernel[i,j] = 0
  im.print(kernel, "kernel")

  see = cv2.erode(see, kernel, iterations=1)
  im.print(see, "seeErode")

  zeroPixels = size*size - cv2.countNonZero(see) #refactorizar

  # regions
  arr = perlinNoise(size, perlinRegions)*256
  im.print(arr, "perlinNoise")

  arr = regionGrower(arr, contryNumber, see, zeroPixels, threshold, thresholdGrowth, distanceFactor,stepsFolder,maxSeedTries, condition)
  im.print(arr, "regionGrower")

  # arr = cv2.medianBlur(arr, medianSize)
  # im.print(arr, "filtroMediana")

  
  # kernel = np.ones((medianSize, medianSize), np.uint8)
  # img_erosion = cv2.erode(arr, kernel, iterations=1)
  # im.print(img_erosion, "erode")
  # img_dilation = cv2.dilate(arr, kernel, iterations=1)
  # im.print(img_dilation, "dilate")

  print(name,"terminado")
  print()

if __name__ == "__main__":


  if os.path.exists(stepsFolder):
    shutil.rmtree(stepsFolder)
  os.makedirs(stepsFolder)


  if os.path.exists(testsFolder):
    shutil.rmtree(testsFolder)
  os.makedirs(testsFolder)
  for i in range(1):
    generateMap(str(i),
      size=128,
      contryNumber=20000,
      #perlinRegions=[(2, 0.5), (5,0.1), (10, 2), (20, 1), (30, 0.5), (100, 0.5)],
      perlinRegions=[(10, 1), (20, 0.5), (30, 0.1),(100, 0.05)],
      perlinSee=[(2, 2), (5,1), (20, 0.5), (100, 0.05)],
      threshold=100,
      thresholdGrowth = lambda x: x+10,
      distanceFactor = lambda x: 0,#2**(x*0.05)*0.01,
      condition = lambda candidate, distance, threshold: candidate + distance < threshold,
      seeLevel=130,
      decreaseFactor=0.9, # en el rango (0,1)
      minEarthSize=0.4, #si es muy bajo puede que no termine por no enconrar huecos libres para semillas
      medianSize=100, # dividir la imagen en este número de partes para calcular el tamaño de la mediana
      #seeMedianSize=50,
      maxSeedTries=100)
  
  print("END")