import os, shutil, numpy as np, matplotlib.image, cv2 # pip install opencv-python
from regionGrower import regionGrower
from perlinNice import perlinNoise

testsFolder = "tests"
stepsFolder = "steps"
finalFolder = "results"


class Img():
  def __init__(s, name):
    s.n=0
    s.name = name
  def print(s,arr, subName):
    fileName = f'{s.name}_{s.n}{subName}.png'
    image = cv2.resize(arr.astype("uint8"), dsize=(2000, 2000), interpolation=cv2.INTER_NEAREST)
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html
    # cmaps= tab20b, tab20c, twilight
    matplotlib.image.imsave(fileName, image, cmap="tab20c")
    #cv2.imwrite(fileName, image)
    s.n+=1

def generateMap(name, size, contryNumber, perlinRegions, perlinSee, threshold, seedThreshold, thresholdGrowth, seeLevel, maxIslands, seeMedianSize, minEarthSize, maxSeedTries, seeColor, isPrint):
  
  im = Img(os.path.join(testsFolder,name))
  imFinal = Img(os.path.join(finalFolder,name))

  # See
  print(name, "comienza")
  seePerlin = (perlinNoise(size, perlinSee)*256).astype("uint8")
  im.print(seePerlin, "perlinSee")

  see, _ = regionGrower(seePerlin, maxIslands, np.ones((size,size)), int(size*size*(1-minEarthSize)),
                     seeLevel, seeLevel, thresholdGrowth, stepsFolder, maxSeedTries, isPrint)
  see = see.astype("bool").astype("uint8") # convertir a array "booleano"
  im.print(see, "boolsee")


  kernelSize = size // seeMedianSize
  kernelSize = kernelSize+kernelSize%2+1 # tiene que ser impar
  see = cv2.medianBlur(see, kernelSize)
  im.print(see, "medianSee")

  zeroPixels = size*size - cv2.countNonZero(see) #refactorizar


  # regions
  arr = ((np.absolute(perlinNoise(size, perlinRegions) - 0.5) * (-1) + 0.5) * 256*2).astype("uint8")
  im.print(arr, "perlinNoise")

  arr, maxColor = regionGrower(arr, contryNumber, see, zeroPixels, threshold, seedThreshold, thresholdGrowth,
                     stepsFolder, maxSeedTries, isPrint)
  arr = arr * ((255-seeColor)/maxColor)+seeColor
  im.print(arr, "regionGrower")
  
  
  # borders
  # operador de Sobel
  # cv2.filter2D trunca los valores negativos a 0, por eso hace falta pasar la máscara en ambos sentidos
  # ddepth = -1, para que tengamos la misma depth que la original, sea lo que sea
  verticalBorder1 = (cv2.filter2D(arr,-1,
    np.array([[ 0, 0, 0],
              [-1, 1, 0],
              [ 0, 0, 0]]))).astype("bool")
  verticalBorder2 = (cv2.filter2D(arr,-1,
    np.array([[ 0, 0, 0],
              [ 1,-1, 0],
              [ 0, 0, 0]]))).astype("bool")
  horizontalBorder1 = cv2.filter2D(arr,-1,
    np.array([[ 0,-1, 0],
              [ 0, 1, 0],
              [ 0, 0, 0]])).astype("bool")
  horizontalBorder2 = cv2.filter2D(arr,-1,
    np.array([[ 0, 1, 0],
              [ 0,-1, 0],
              [ 0, 0, 0]])).astype("bool")
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

  for i in range(100):
    generateMap(str(i),
      size=800,
      contryNumber=20,
      perlinRegions=[(6, 1), (10, 1), (20, 0.5),(100, 0.1)],
      #perlinRegions=[(6, 1), (10, 0.5), (20, 1), (40, 1),(100, 0.1)],
      #perlinSee=[(2,10),(3,10),(10, 2), (20, 2), (40, 1), (100, 0.5)],
      perlinSee=[(2, 2), (5,1), (20, 0.5), (100, 0.05)],
      threshold=230,
      seedThreshold=20,
      thresholdGrowth = lambda x: x+1,
      seeLevel=10,
      maxIslands=4,
      seeMedianSize=150, # dividir la imagen en este número de partes para calcular el tamaño de la mediana
      minEarthSize=0.6, #si es muy bajo puede que no termine por no enconrar huecos libres para semillas
      maxSeedTries=10000,
      seeColor = 20,
      isPrint = False)
  
  print("END")