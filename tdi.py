import random, math, os, shutil, numpy as np
import matplotlib.image as img
import cv2 # pip install opencv-python
from regionGrower import regionGrower
from perlinNice import perlinNoise
#from decimal import * # me ha pasado un poco con el tamaño de los numbers

testsFolder = "tests"
stepsFolder = "steps"
finalFolder = "results"


class Img():
  def __init__(s, name):
    s.n=0
    s.name = name
  def print(s,arr, subName):
    img.imsave(f'{s.name}_{s.n}{subName}.png', cv2.resize(arr, dsize=(2000, 2000), interpolation=cv2.INTER_NEAREST))
    s.n+=1

def generateMap(name, size, contryNumber, perlinRegions, perlinSee, threshold, thresholdGrowth, distanceFactor, seeLevel,decreaseFactor, minEarthSize, medianSize, maxSeedTries, condition, isPrint):
  
  im = Img(os.path.join(testsFolder,name))
  imFinal = Img(os.path.join(finalFolder,name))

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

  see = cv2.medianBlur(see, medianSize)
  im.print(see, "seeMediana")
  
  # kernel = np.ones((medianSize, medianSize), np.uint8)
  # radius = medianSize//2
  # for i in range(medianSize):
  #   for j in range(medianSize):
  #     if ((i-radius)**2+(j-radius)**2)**0.5 > radius:
  #       kernel[i,j] = 0
  # im.print(kernel, "kernel")

  # see = cv2.erode(see, kernel, iterations=1)
  # im.print(see, "seeErode")

  zeroPixels = size*size - cv2.countNonZero(see) #refactorizar

  # regions
  arr = ((np.absolute(perlinNoise(size, perlinRegions) - 0.5) * (-1) + 0.5) * 256*2).astype("uint8")
  im.print(arr, "perlinNoise")

  arr = regionGrower(arr, contryNumber, see, zeroPixels, threshold, thresholdGrowth, distanceFactor,stepsFolder,maxSeedTries, condition, isPrint)
  im.print(arr, "regionGrower")

  # arr = cv2.medianBlur(arr, medianSize)
  # im.print(arr, "filtroMediana")

  
  # kernel = np.ones((medianSize, medianSize), np.uint8)
  # img_erosion = cv2.erode(arr, kernel, iterations=1)
  # im.print(img_erosion, "erode")
  # img_dilation = cv2.dilate(arr, kernel, iterations=1)
  # im.print(img_dilation, "dilate")

  imFinal.print(arr, "")
  print(name,"terminado")
  print()

def prepareFolder(name):
  if os.path.exists(name):
    shutil.rmtree(name)
  os.makedirs(name)

if __name__ == "__main__":

  prepareFolder(stepsFolder)
  prepareFolder(testsFolder)
  prepareFolder(finalFolder)

  for i in range(100):
    generateMap(str(i),
      size=400,
      contryNumber=20,
      perlinRegions=[(6, 1), (10, 1), (20, 0.5),(100, 0.1)],
      perlinSee=[(2, 2), (5,1), (20, 0.5), (100, 0.05)],
      threshold=180,
      thresholdGrowth = lambda x: x*1.01,
      distanceFactor = lambda x: 2**(x*0.01)*0.01,
      condition = lambda candidate, distance, threshold: candidate + distance < threshold,
      seeLevel=130,
      decreaseFactor=0.9, # en el rango (0,1)
      minEarthSize=0.4, #si es muy bajo puede que no termine por no enconrar huecos libres para semillas
      medianSize=100, # dividir la imagen en este número de partes para calcular el tamaño de la mediana
      #seeMedianSize=50,
      maxSeedTries=100,
      isPrint = False)
  
  print("END")