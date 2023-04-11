import os, shutil, numpy as np
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
    fileName = f'{s.name}_{s.n}{subName}.png'
    image = cv2.resize(arr, dsize=(2000, 2000), interpolation=cv2.INTER_NEAREST)
    img.imsave(fileName, image)
    #cv2.imwrite(fileName, image)
    s.n+=1

def calculateKerneSize(size, kernelSize):
  kernelSize = size // kernelSize
  return kernelSize+kernelSize%2+1 # tiene que ser impar

def generateMap(name, size, contryNumber, perlinRegions, perlinSee, threshold, seedThreshold, thresholdGrowth, seeLevel, maxIslands, seeMedianSize, minEarthSize, maxSeedTries, minSize, isPrint):
  
  im = Img(os.path.join(testsFolder,name))
  imFinal = Img(os.path.join(finalFolder,name))

  # See
  print(name, "comienza")
  seePerlin = (perlinNoise(size, perlinSee)*256).astype("uint8")
  im.print(seePerlin, "perlinSee")

  see = regionGrower(seePerlin, maxIslands, np.ones((size,size)), int(size*size*(1-minEarthSize)),
                     seeLevel, seeLevel, thresholdGrowth, stepsFolder,maxSeedTries, 0, isPrint)
  see = see.astype("bool").astype("uint8") # convertir a array "booleano"
  im.print(see, "boolsee")

  see = cv2.medianBlur(see, calculateKerneSize(size,seeMedianSize))
  im.print(see, "medianSee")

  zeroPixels = size*size - cv2.countNonZero(see) #refactorizar


  # regions
  arr = ((np.absolute(perlinNoise(size, perlinRegions) - 0.5) * (-1) + 0.5) * 256*2).astype("uint8")
  im.print(arr, "perlinNoise")

  arr = regionGrower(arr, contryNumber, see, zeroPixels, threshold, seedThreshold, thresholdGrowth,
                     stepsFolder, maxSeedTries, minSize, isPrint)
  im.print(arr, "regionGrower")
  
  
  # borders
  # cv2.filter2D trunca los valores negativos a 0, por eso hace falta pasar la máscara en ambos sentidos
  # ddepth = -1, para que tengamos la misma depth que la original, sea lo que sea
  verticalBorder1 = (cv2.filter2D(arr,-1,
    np.array([[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]]))).astype("bool")
  verticalBorder2 = (cv2.filter2D(arr,-1,
    np.array([[ 1, 0,-1],
              [ 2, 0,-2],
              [ 1, 0,-1]]))).astype("bool")
  horizontalBorder1 = cv2.filter2D(arr,-1,
    np.array([[-1,-2,-1],
              [ 0, 0, 0],
              [ 1, 2, 1]])).astype("bool")
  horizontalBorder2 = cv2.filter2D(arr,-1,
    np.array([[ 1, 2, 1],
              [ 0, 0, 0],
              [-1,-2,-1]])).astype("bool")
  borders = (~(verticalBorder1 | verticalBorder2 | horizontalBorder1 | horizontalBorder2)).astype("uint8")
  im.print(borders, "borders")
  
  arr = arr * borders
  im.print(arr, "borderedMap")

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

  for i in range(10):
    generateMap(str(i),
      size=500,
      contryNumber=20,
      perlinRegions=[(6, 1), (10, 1), (20, 0.5),(100, 0.1)],
      #perlinRegions=[(6, 1), (10, 0.5), (20, 1), (40, 1),(100, 0.1)],
      perlinSee=[(2,10),(3,10),(10, 2), (20, 2), (40, 1), (100, 0.5)],
      #perlinSee=[(2, 2), (5,1), (20, 0.5), (100, 0.05)],
      threshold=230,
      seedThreshold=20,
      thresholdGrowth = lambda x: x+1,
      seeLevel=10,
      maxIslands=4,
      seeMedianSize=150, # dividir la imagen en este número de partes para calcular el tamaño de la mediana
      minEarthSize=0.6, #si es muy bajo puede que no termine por no enconrar huecos libres para semillas
      maxSeedTries=10000,
      minSize = 0.01,
      isPrint = False)
  
  print("END")