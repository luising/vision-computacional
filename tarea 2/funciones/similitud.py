"""Segmentacion de similitud."""
import numpy as np
import funciones.LM as lm
import cv2

arrayNeighbor = 0
ArrayMap = 0
aEdge = 0
row, column = 0, 0
Neighbor = isFirst = firstP = 1
newPivote = 0
umbral = 0
pixels = 0


def setParameter(imagen):
    """Agregar datos de imagen."""
    global pixels, arrayNeighbor, ArrayMap, aEdge
    global pivote, firstP, newPivote
    arrayNeighbor = np.zeros(shape=imagen.size())
    ArrayMap = np.zeros(shape=imagen.size())
    aEdge = np.zeros(shape=imagen.size())
    row, column = imagen.size()
    pixels = imagen.pixels
    ArrayMap[0][0] = 1
    newPivote = 0


def searchNeighbor():
    """Buscar Vecindario."""
    global pixels, arrayNeighbor, ArrayMap, aEdge
    global pivote, firstP, newPivote
    while(not (ArrayMap != 1).all()):
        activos = [np.where(ArrayMap == 1)]
        for y, x in activos:
            y, x = y[0], x[0]
            xf = x - 1 if x > 0 else 0
            yf = y - 1 if y > 0 else 0
            dif = abs(pixels[y, x] - pivote)
            if dif > umbral:
                if firstP:
                    newPivote = y, x
                    firstP = 0
                aEdge[y, x] = 255
                ArrayMap[y, x] = 0
            else:
                v = ArrayMap[yf:y + 2, xf:x + 2]
                v[v == 0] = 1
                ArrayMap[yf:y + 2, xf:x + 2] = v
                ArrayMap[y, x] = 2
                if not (v == 1).any():
                    notR = [np.where(ArrayMap == 0)]
                    try:
                        ArrayMap[notR[0][0][0], notR[0][1][0]] = 1
                        newPivote = notR[0][0][0], notR[0][1][0]
                        firstP = 0
                    except BaseException:
                        return


def similitud(pumbral=0):
    """Funcion de similitud."""
    umbral = pumbral
    global pixels, arrayNeighbor, ArrayMap
    global pivote, firstP, newPivote, isFirst, Neighbor
    global aEdge
    ArrayMap[0][0] = 1
    while(not (ArrayMap == -1).all()):
        if isFirst:
            isFirst = 0
            pf, pc = 0, 0
        else:
            pf, pc = newPivote
            firstP = 1
        pivote = pixels[pf, pc]
        ArrayMap[pf, pc] = 1
        searchNeighbor()
        # print("encontrado ->", Neighbor)
        arrayNeighbor[np.where(ArrayMap == 2)] = Neighbor
        Neighbor += 1
        ArrayMap[np.where(ArrayMap == 2)] = -1
    lm.saveMatriz(ArrayMap, "borde.txt")
    cv2.imwrite("bordes.png", aEdge)
    lm.saveMatriz(arrayNeighbor, "v.txt")


def umbral16(pixels, tipo):
    """Umbral de corte."""
    lmin = 0
    lmax = 255
    for f, fila in enumerate(pixels):
        for c, pixel in enumerate(fila):
            maximo = 255 // tipo
            minimo = 0
            rango = maximo
            while pixels[f, c] >= maximo:
                minimo = maximo
                maximo += rango
            if(maximo < lmax or minimo < lmin):
                umbral = (maximo + minimo) // 2
                pixels[f, c] = minimo if(pixel < umbral) else maximo
            else:
                pixel = 0 if minimo == lmin else pixel
                pixel = 255 if maximo == lmax else pixel
                pixels[f, c] = pixel
    return pixels
