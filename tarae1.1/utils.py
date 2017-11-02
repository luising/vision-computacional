from PIL import Image


def saveAllChanges():
    global lastImage
    i = "output.png"
    a, width, height, pixels = imageToPixelsL(lastImage)
    saveImage((width, height), pixels, i, show=True)
    return


def imageToPixelsL(inputImage):
    i = Image.open(inputImage)
    i = i.convert('L')
    pixels = i.load()
    w, h = i.size
    pixelsL = list()
    for x in range(h):
        for y in range(w):
            pixel = pixels[y, x]
            pixelsL.append(pixel)
    return i, w, h, pixelsL, pixels


def pixels2dTopixelsL(pixels, w, h):
    pixelsL = list()
    for x in range(h):
        for y in range(w):
            pixel = pixels[y, x]
            pixelsL.append(pixel)
    return pixelsL


def saveImage(size, pixels, outputName, show=False):
    im = Image.new('L', size)
    im.putdata(pixels)
    im.save(outputName)
    if(show): im.show()
    return


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
