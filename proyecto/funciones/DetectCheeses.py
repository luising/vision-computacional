import numpy as np
from funciones.imageL import *
from funciones.LM import *
from funciones.filtrosS import umbralb, dilatacion, erosion, skeleton


def detection(imagen):
    mmxpixels = 3.77952755905511
    # umbralizacion binaria de la imagen
    a, width, height, pixelsL, pixels2d = imageToPixelsL(imagen)
    pixelsL = umbralb(pixelsL, 175)
    # lista a matriz numpy
    pixels = listTonumpy2d(pixelsL, (height, width), np.uint8)
    # metodo dilatacion
    pixels = dilatacion(pixels, (3, 3), 3)
    # metodo erosion
    pixels = erosion(pixels, (2, 2), 9)
    savecv("procesamiento/Apre-ad.png", pixels)
    # metodo de adelgazamiento
    pixels = skeleton("procesamiento/Apre-ad.png", "procesamiento/Badelgazamiento.png")
    # Seguimiento del segmento primitivo
    mapaS = np.zeros(shape=pixels.shape)
    for a in range(height):
        for b in range(width):
            if pixels[a, b] == 1:
                v = sumM(neighboring3x3(pixels, a, b, 0))
                if v == 0:
                    pixels[a][b] = 0
                else:
                    mapaS[a][b] = v
    PrimitiveSegments = buscarCamino(mapaS, 1)
    numSegment = len(PrimitiveSegments)
    for n in range(numSegment):
            r = PrimitiveSegments[n][1][0]
            c = PrimitiveSegments[n][1][1]
            if (r, c) == (0, 0): continue
            for x in range(numSegment):
                if n != x:
                    r2 = PrimitiveSegments[x][1][0]
                    c2 = PrimitiveSegments[x][1][1]
                    if((r - 2 <= r2 and r + 2 >= r2) or (c - 2 <= c2 and c + 2 >= c2)):
                        PrimitiveSegments[n] = [
                            PrimitiveSegments[n][0],
                            (r2, c2),
                            (PrimitiveSegments[n][2] + PrimitiveSegments[x][2])
                        ]
                        PrimitiveSegments[x] = [(0, 0), (0, 0), 0]
    cortes = 0
    listT = list()
    for x in PrimitiveSegments:
            tamaño = x[2]
            if(tamaño != 0 and tamaño > 40):
                mm = tamaño / mmxpixels
                listT.append("segmento: " + str(round(mm, 2)) + " mm")
                cortes += 1
    print("numero de cortes de queso: ", cortes)
    return [
        ("numero de cortes de queso: " + str(cortes)),
        listT
    ]


if __name__ in "__main__":
    detection()
