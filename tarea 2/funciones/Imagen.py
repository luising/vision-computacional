import numpy as np
import LM as lm
import Filtros as f
import cv2


class Imagen(object):
    """Clase imagen manipular imagenes solo escala grises ."""

    def __init__(self, nameImage, mode):
        self.mode = mode
        self.nameImage = nameImage
        self.ToPixels(mode)

    # abrir imagen
    def imagecv(self, image, mode):
        self.mode = mode
        self.image = image
        self.ToPixels(mode)

    # guardar Imagen
    def saveAllChanges(self):
        a, width, height, pixels = self.imageToPixelsL(self.image)
        self.saveImage((width, height), pixels, "output.png", show=True)
        return

    def savecv(self, path):
        cv2.imwrite(path, self.pixels)

    def saveImage(size, pixels, outputName, show=False):
        # im = Image.new('L', size)
        # im.putdata(pixels)
        # im.save(outputName)
        # if(show): im.show()
        pass

    def ToPixels(self, mode="RGB"):
        if mode != "RGB":
            imagen = cv2.imread(self.nameImage, 0)
        self.pixels = imagen
        self.h, self.w = imagen.shape
        self.listpixels = list()
        for y in range(self.h):
            for x in range(self.w):
                self.listpixels.append(self.pixels[y, x])

    def size(self):
        return (self.h, self.w)

    def pixels2dTopixelsL(self):
        listpixels = list()
        for y in range(self.h):
            for x in range(self.w):
                listpixels.append(self.pixels[y, x])

    def calcularVecinosSurEste(pixels, b, a):
        # pixeles = (lista de listas) contiene todos los pixeles de la imagen
        # indice = (int) es la posicion del pixel actual
        # ancho = (int) es el ancho de la imagen
        # primero el izquiero
        pix_der = 0
        pix_abajo = 0
        m = []
        try:
            # print("izq", pixels[b - 1, a])
            pix_izq = pixels[b - 1, a]
        except:
            pass
        try:
            # print("der", pixels[b + 1, a])
            pix_der = pixels[b + 1, a]
        except:
            pass
        try:
            # print("arr", pixels[b, a + 1])
            pix_arriba = pixels[b, a + 1]
        except:
            pass
        try:
            # print("ab", pixels[b, a - 1])
            pix_abajo = pixels[b, a - 1]
        except:
            pass

        m.append(pix_izq)
        m.append(pix_der)
        m.append(pix_arriba)
        m.append(pix_abajo)
        # print(m)
        return m

    def vecinos3x3(pixels, b, a):
        pix_izq, pix_der, pix_arriba, pix_abajo, arriba_izq, arriba_der, abajo_izq, abajo_der = [0 for _ in range(8)]

        m = [[0 for _l in range(3)] for _p in range(3)]
        try:
            pix_izq = pixels[b - 1, a]
        except:
            pass
        try:
            pix_der = pixels[b + 1, a]
        except:
            pass
        try:
            pix_arriba = pixels[b, a - 1]
        except:
            pass
        try:
            pix_abajo = pixels[b, a + 1]
        except:
            pass
        try:
            arriba_izq = pixels[b - 1, a - 1]
        except:
            pass
        try:
            arriba_der = pixels[b + 1, a - 1]
        except:
            pass
        try:
            abajo_izq = pixels[b - 1, a + 1]
        except:
            pass
        try:
            abajo_der = pixels[b + 1, a + 1]
        except:
            pass

        b, a = 1, 1

        m[b - 1][a] = pix_izq
        m[b + 1][a] = pix_der
        m[b][a - 1] = pix_arriba
        m[b][a + 1] = pix_abajo
        m[b - 1][a - 1] = arriba_izq
        m[b + 1][a - 1] = arriba_der
        m[b - 1][a + 1] = abajo_izq
        m[b + 1][a + 1] = abajo_der
        return pix_izq, pix_der, pix_arriba, pix_abajo, arriba_izq, arriba_der, abajo_izq, abajo_der

    def umbralbinary(self, beta):
        self.listpixels = f.umbralbinary(self.listpixels, beta)
        self.pixels = lm.listTonumpy2d(self.listpixels, (self.w, self.h), np.uint8)
