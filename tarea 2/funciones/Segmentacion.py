from Imagen import *
import numpy as np

def umbral16(pixels, tipo):
    lmin=0
    lmax=255
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
def Similitud(imagen):
    # i = umbral16(imagen.pixels, 16)
    # cv2.imwrite("im.png", i)
    umbral = 10
    neighbor = 1
    pixels = np.array(imagen.pixels)
    neighbors = np.zeros(shape=imagen.size())
    mapp = np.zeros(shape=imagen.size())
    r, c = imagen.size()
    for y in range(r):
        for x in range(c):
            if x > 0 and y > 0:
                n = x + 1
                m = y + 1
                try:
                    h = np.abs(pixels[y - 1:y + 2,n - 1:n + 2] - pixels[y - 1:y + 2,x - 1:x + 2])
                    v = np.abs(pixels[m - 1:m + 2,x - 1:x + 2] - pixels[y - 1:y + 2,x - 1:x + 2])
                    mapp[y - 1:y + 2,x - 1:x + 2] = h + v
                except:
                    pass
                v = mapp[y - 1:y + 2, x - 1:x + 2]
                v[v > umbral] = 255
                v[v < umbral] = 0
                mapp[y - 1:y + 2, x - 1:x + 2] = v
    # for y in range(r):
    #     for x in range(c):
    #         if x > 0 and y > 0:
    #             mv = neighbors[y - 1:y + 2,x - 1:x + 2]
    #             ve = np.unique(mv)
    #             lve = len(ve)
    #             if(lve == 2):
    #                 neighbors[y, x] = ve[1]
    #         elif(y == 0):
    #             if mapp[y, x] == 0:
    #                 neighbor += 1
    #             neighbors[y, x] = neighbor
    lm.saveMatriz(pixels, "pixels.txt")
    lm.saveMatriz(mapp, "borde.txt", 1)
    lm.saveMatriz(neighbors, "v.txt", 1)
    cv2.imwrite("bordes.png", mapp)

Similitud(Imagen("p.png", 'L'))
