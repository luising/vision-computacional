import cv2
from math import log
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
from skimage import io
from scipy import misc
from skimage.util import invert


# filtros de Imagenes
# tomar en cuenta que deben ser matriz de escala grises por el momento
def escala_grises(pixels):
        return pixels


def invertir(pixels):
    for a, pixel in enumerate(pixels):
        pixels[a] = 255 - pixel
    return pixels


def clarado(pixels, c=2, lmin=0, lmax=255):
    for a, pixel in enumerate(pixels):
        pixels[a] = 255 if(pixel * c > lmax) else pixel * c
    return pixels


def copiar(pixels):
    return pixels


def brillo(pixels, c=2, lmin=0, lmax=255):
    for a, pixel in enumerate(pixels):
        pixels[a] = 255 if(pixel + c > lmax) else pixel + c
    return pixels


def Acontraste(pixels, gama, beta):
    for a, pixel in enumerate(pixels):
        pixels[a] = (pixel * gama) + beta
    return pixels


def Rcontraste(pixels, gama, beta):
    for a, pixel in enumerate(pixels):
        pixels[a] = (pixel / gama) - beta
    return pixels


def slicing(l, n):
    print("l", len(l))
    return [l[a:a + n] for a in range(0, len(l), n)]


def threshold(img, thr, width, height):
    # Límites de procesado en x
    x_min, x_max = 0, width
    # Límites de procesado en y
    y_min, y_max = 0, height
    # Imagen de salida
    img_out = np.zeros(width * height)
    # Procesado de la imagen
    loc = 0
    # Posición del "pixel" actual
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            loc = y * width + x
            if img[loc] > thr: img_out[loc] = 255
            else:
                img_out[loc] = 0
    return img_out


def otsu_threshold(histogram):
    # Vector de probabilidad acumulada.
    omega = np.zeros(256)
    # Vector de media acumulada.
    mean = np.zeros(256)
    # Partiendo del histograma normalizado se calculan la probabilidad
    # acumulada (omega) y la media acumulada (mean).
    omega[0] = histogram[0]
    for i in range(len(histogram)):
        omega[i] = omega[i - 1] + histogram[i]
        mean[i] = mean[i - 1] + i * histogram[i]
    sigmaB2 = 0
    mt = mean[len(histogram) - 1]  # Valor de la intensidad media de la imagen
    sigmaB2max = 0
    T = 0
    for i in range(len(histogram)):
        clase1 = omega[i]
        clase2 = 1 - clase1
        if clase1 != 0 and clase2 != 0:
            m1 = mean[i] / clase1
            m2 = (mt - mean[i]) / clase2
            sigmaB2 = (clase1 * (m1 - mt) * (m1 - mt) + clase2 * (m2 - mt) * (m2 - mt))
            if sigmaB2 > sigmaB2max:
                sigmaB2max = sigmaB2
                T = i
    return int(T)


def Varianza(pixels, imagen, w, h, lmin=0, lmax=255):
    imag = Image.open(imagen)
    imagL = imag.convert("L")
    hist = imagL.histogram()
    thr = otsu_threshold(hist)
    img_thr = threshold(imagL.getdata(), thr, w, h)
    plt.show(img_thr.reshape(h, w))
    return img_thr


def mediana(pixels, w, h, to2d=False):
    for a in range(h):
        for b in range(w):
            temp = calcularVecinosCruz(pixels, b, a)
            temp.sort()
            n = len(temp)
            pixels[b, a] = int(temp[int(n / 2 - 1)] + temp[int(n / 2)] / 2 if n % 2 == 0 else temp[int(n / 2)])
    if not to2d:
        pixels = pixels2dTopixelsL(pixels, w, h)
    return pixels


def modal(pixels, w, h):
    for a in range(h):
        for b in range(w):
            if a or b > 0 or a < h or b < w:
                temp = calcularVecinosCruz(pixels, b, a)
                temp.sort()
                repeticiones = max(temp.count(i) for i in temp)
                modas = []
                for i in temp:
                    if temp.count(i) == repeticiones and i not in modas:
                        modas.append(i)
                if(len(modas) != 1):
                    pixels[b, a] = modas[1]
    pixels = pixels2dTopixelsL(pixels, w, h)
    return pixels


def calcularVecinosCruz(pixels, b, a):
    # pixeles = (lista de listas) contiene todos los pixeles de la imagen
    # indice = (int) es la posicion del pixel actual
    # ancho = (int) es el ancho de la imagen
    # primero el izquiero
    pix_izq = 0
    pix_der = 0
    pix_arriba = 0
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


def MaxProb(pixels, imagen):
    imag = Image.open(imagen)
    imagL = imag.convert("L")
    hist = imagL.histogram()
    mayor = (0, 0)
    for i, h in enumerate(hist):
        pm = h**3 * (1 - h)**2
        if pm > mayor[1]:
            mayor = tuple((i, pm))
    for a, pixel in enumerate(pixels):
        pixels[a] = 255 if pixel > mayor[0] else 0
    return pixels


def valle_global(pixels, imagen):
    imag = Image.open(imagen)
    imagL = imag.convert("L")
    hist = imagL.histogram()
    f = max(hist)
    umbral = np.mean([i for i, h in enumerate(hist) if h == f])
    D = 30
    for i, p in enumerate(pixels):
        pixels[i] = 255 if umbral > p - D and umbral < p + D else 0
    return pixels


def umbralbinary(pixels, beta):
        for a, p in enumerate(pixels):
            pixels[a] = 255 if(p > beta) else 0
        return pixels


def calcularPixel(tipo, pixel, lmin=0, lmax=255):
    maximo = 255 / tipo
    minimo = 0
    rango = maximo
    while pixel >= maximo:
        minimo = maximo
        maximo += rango
    if(maximo < lmax or minimo < lmin):
        umbral = (maximo + minimo) / 2
        return minimo if(pixel < umbral) else maximo
    else:
        pixel = 0 if minimo == lmin else pixel
        pixel = 255 if maximo == lmax else pixel
        return pixel


def umbral(pixels, tipo):
        for a, pixel in enumerate(pixels):
            pixels[a] = int(calcularPixel(tipo, pixel))
        return pixels


def shiftingI(pixels, w, h):
    for a in range(1, h - 1):
        for b in range(1, w - 1):
            grad = pixels[b, a] - pixels[b - 1, a]
            pixels[b, a] = int(grad * pixels[b + 1, a] / float(pixels[b - 1, a] if pixels[b - 1, a] > 0 else 1))
    return pixels2dTopixelsL(pixels, w, h)


def shiftingV(pixels, w, h):
    for a in range(1, h - 1):
        for b in range(1, w - 1):
            grad = pixels[b, a] - pixels[b, a - 1]
            pixels[b, a] = int(grad * pixels[b, a + 1] / float(pixels[b, a - 1] if pixels[b, a - 1] > 0 else 1))
    return pixels2dTopixelsL(pixels, w, h)


def shiftingD(pixels, w, h):
    for a in range(1, h - 1):
        for b in range(1, w - 1):
            grad = pixels[b, a] - pixels[b - 1, a - 1]
            pixels[b, a] = int(grad * pixels[b - 1, a + 1] / float(pixels[b - 1, a - 1] if pixels[b - 1, a - 1] > 0 else 1))
    return pixels2dTopixelsL(pixels, w, h)


def Sal_Pimienta(pixels, w, h):
        for a in range(h):
            for b in range(w):
                temp = calcularVecinosCruz(pixels, b, a)
                temp.sort()
                n = len(temp)
                pixels[b, a] = int(temp[int(n / 2 - 1)] + temp[int(n / 2)] / 2 if n % 2 == 0 else temp[int(n / 2)])
        pixels = pixels2dTopixelsL(pixels, w, h)
        return pixels


refPt = []
cropping = False
image = 0


def adaptativo(pixels, imagen, w, h):
    global image, refpt
    image = cv2.imread(imagen, cv2.IMREAD_GRAYSCALE)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)
    # pixels = mediana(pixels, w, h, True)
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()
            break
    if len(refPt) == 1:
        xp, yp = refPt[0][0], refPt[0][1]
        umbral = pixels[xp, yp]
        print("origen ", umbral)
        for a in range(h):
            for b in range(w):
                pixels[b, a] = 255 if umbral == pixels[b, a] else 0
    pixels = pixels2dTopixelsL(pixels, w, h)
    return pixels


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        print(refPt)
        cropping = True

    # check to see if the left mouse button was released
    # draw a rectangle around the region of interest
    # cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
    # cv2.imshow("image", image)


def entropia(pixels, imagen, w, h):
    total = len(pixels)
    imag = Image.open(imagen)
    imagL = imag.convert("L")
    hist = imagL.histogram()
    D = 2
    sfp = 0
    sfpb = 0
    for i, h in enumerate(hist):
        fp = hist[i] / total
        if fp == 0: fp = 1
        sfp -= fp * log(fp)
        if i != 0:
            sfpb -= fp * log(fp)
    t = sfp + sfpb
    for a, p in enumerate(pixels):
        isEntro = False
        if not(t > p - D and t < p + D):
            isEntro = True
        pixels[a] = 0 if isEntro else 255
    return pixels


# metodo skimage
# pixels puede ser direccion de la imagen o matriz entre 0 y 255(0,1)
# path parametro opcional que permite guardar el resultado en la direccion que mandaste
# retorna matriz boleano
def skeleton(pixels, path=0):
    if type(pixels) == str:
        image = io.imread(pixels, 1)
    else:
        image = pixels
    # invertir imagen
    image = invert(image)
    for b, f in enumerate(image):
        for a, p in enumerate(f):
            image[b][a] = 0 if image[b][a] == 255 else 1
    # aplicar skeletonize
    skeleton = skeletonize(image)
    if path != 0:
        misc.imsave(path, skeleton)
    return skeleton


# metodo dilatacion de una imagen
# disminuye el grosor sirve para afinar los elementos de una imagen
# pixels matriz de opencv
# wh tuple de las dimenciones de vecinos .ej (3, 3)
# i entero nuemro de iteraciones que realizara
def dilatacion(pixels, wh, i):
    # metodo dilatacion
    kernel = np.ones(wh, np.uint8)
    pixels = cv2.dilate(pixels, kernel, iterations=i)
    return pixels


# metodo erosion de una imagen
# aumenta el grosor sirve eliminar huecos de una imagen
# pixels matriz de opencv
# wh tuple de las dimenciones de vecinos .ej (3, 3)
# i entero nuemro de iteraciones que realizara
def erosion(pixels, wh, i):
    kernel = np.ones(wh, np.uint8)
    pixels = cv2.erode(pixels, kernel, iterations=i)
    return pixels
