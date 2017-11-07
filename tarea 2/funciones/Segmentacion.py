from Imagen import *
import numpy as np
import collections

def Discontinuidad(imagen):
    intencidad = 255
    borde = 0
    h, w = imagen.size()

    print(h, w)
    mapaH1 = [[(int(imagen.pixels[y, x + 1]) - int(imagen.pixels[y, x])) for x in range(w - 1)] for y in range(h)]
    mapaH2 = [[(abs(int(mapaH1[y][x + 1]) - int(mapaH1[y][x]))) for x in range(w - 2)] for y in range(h)]

    mapaV1 = [[(int(imagen.pixels[y + 1, x]) - int(imagen.pixels[y, x])) for x in range(w)] for y in range(h - 1)]
    mapaV2 = [[(abs(int(mapaV1[y + 1][x] - mapaV1[y][x]))) for x in range(w)] for y in range(h - 2)]

    # listofirst = [0 for _ in range(h - 2)]
    print("DH1:", len(mapaH1), len(mapaH1[0]))
    print("DH2:", len(mapaH2), len(mapaH2[0]))
    print("DV1:", len(mapaV1), len(mapaV1[0]))
    print("DV2:", len(mapaV2), len(mapaV2[0]))

    for y in range(h - 2):
        for x in range(w - 2):
            v = mapaH2[y][x]
            ho = mapaV2[y][x]
            hod = mapaV2[y][x + 1]
            if v == ho:
                imagen.pixels[y, x] = intencidad
                imagen.pixels[y, x + 1] = intencidad
                imagen.pixels[y, x + 2] = intencidad
            else:
                imagen.pixels[y, x] = borde
                # imagen.pixels[y, x + 1] = borde
                # imagen.pixels[y, x + 2] = borde
    lm.printM(imagen.pixels)
    imagen.savecv("new.png")
    return imagen

def Similitud(imagen):
    umbral = 2
    neighbor = 1
    pixels = np.array(imagen.pixels)
    neighbors = np.zeros(shape=imagen.size())
    mapp = np.zeros(shape=imagen.size())
    r, c = imagen.size()
    for y in range(r):
        for x in range(c):
            if x > 0 and y > 0:
                mapp[y - 1:y + 2,x - 1:x + 2] = pixels[y - 1:y + 2,x - 1:x + 2] - pixels[y, x]
                v = mapp[y - 1:y + 2, x - 1:x + 2]
                v[v < umbral] = 255
                v[v < 255] = 0
                mapp[y - 1:y + 2, x - 1:x + 2] = v

    for y in range(r):
        for x in range(c):
            if x > 0 and y > 0:
                mv = neighbors[y - 1:y + 2,x - 1:x + 2]
                ve = np.unique(mv)
                lve = len(ve)
                if(lve == 2):
                    neighbors[y, x] = ve[1]
                
                # if pixels[y, x] == 0:
                #     neigbors += 1
                # n[] = neigbors
                # mv = n
                # neighbors[y - 1:y + 2,x - 1:x + 2] = mv
            elif(y == 0):
                if mapp[y, x] == 0:
                    neighbor += 1
                neighbors[y, x] = neighbor


    lm.saveMatriz(pixels, "pixels.txt")
    lm.saveMatriz(mapp, "borde.txt", 1)
    lm.saveMatriz(neighbors, "v.txt", 1)
    cv2.imwrite("bordes.png", mapp)
    cv2.imwrite("neig.png", neighbors)

Similitud(Imagen("p.png", 'L'))
