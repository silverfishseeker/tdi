
import random, numpy as np

def subPerlin(size, step): # genera una frecuencia de ruidete con valores en el intervalo [0,1)
    if step <= 0: raise ValueError("menor o igual que 0")
    mapa = np.zeros([(size//step+1)*step+1]*2) # necesitamos hueco de más para los "pivotes" exteriores
    for i in range(size//step+2):
        for j in range(size//step+2):
            mapa[i*step,j*step] = random.random()
            if i > 0 and j > 0:
                for i2 in range(step):
                    for j2 in range(step):
                        #Interpolación bilineal
                        x2 = i  * step
                        x1 = x2 - step
                        y2 = j  * step
                        y1 = y2 - step
                        mapa[x1+i2,y1+j2] = (
                            mapa[x1,y1]*(step-i2)*(step-j2)
                            +mapa[x2,y1]*i2*(step-j2)
                            +mapa[x1,y2]*(step-i2)*j2
                            +mapa[x2,y2]*i2*j2
                            )/step/step
    return mapa[:size,:size]

def perlinNoise(size, stepsWeights):
    """
    stepsWeights: lista de duplas de números. Cada dupla es: (número de steps, peso de esa frecuencia)
    """
    totalWeight = sum([x[1] for x in stepsWeights])
    return np.asarray([subPerlin(size, x[0])*(x[1]/totalWeight) for x in stepsWeights], dtype=float).sum(axis=0)

def perlinNoiseFreq(size, stepsFreqs):
    """
    Igual que perlinNoise pero por fecuencias en vez de steps
    """
    return perlinNoise(size, tuple((size//x[0], x[1]) for x in stepsFreqs)) 