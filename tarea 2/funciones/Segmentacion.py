from Imagen import *

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
    vecindario = 255
    borde = 0
    beta = 50
    h, w = imagen.size()

    print(h, w)
    mapaH2 = [[(abs(int(imagen.pixels[y][x + 1]) - int(imagen.pixels[y][x]))) for x in range(w - 1)] for y in range(h)]
    mapaV2 = [[(abs(int(imagen.pixels[y + 1][x]) - int(imagen.pixels[y][x]))) for x in range(w)] for y in range(h - 1)]
    print("DH2:", len(mapaH2), len(mapaH2[0]))

    asign = [[0 for _ in range(h - 1)] for d in range(w - 1)]
    print(asign)
    for y in range(h - 1):
        for x in range(w - 1):
            d1 = mapaH2[y][x]
            d1 = 255 if(d1 > 255) else d1
            if d1 <= beta:
                imagen.pixels[y, x] = vecindario
            else:
                imagen.pixels[y, x] = borde
    for x in range(w - 1):
        for y in range(h - 1):
            dv1 = mapaV2[y][x]
            dv1 = 255 if(dv1 > 255) else dv1
            if dv1 > beta:
                imagen.pixels[y, x] = borde

    # lm.printM(imagen.pixels)
    imagen.savecv("new.png")
Similitud(Imagen("w.png", 'L'))
