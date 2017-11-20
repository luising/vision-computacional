"""Script prueba de Detenccion."""
import numpy as np
import cv2

import funciones.Similitud as seg
import funciones.LM as lm
from funciones.Imagen import Imagen

# carga de imagen
imagen = Imagen("p.png", 'L')
pixels = seg.umbral16(imagen.pixels, 16)
cv2.imwrite("im.png", pixels)
pixels = np.array(pixels)
lm.saveMatriz(pixels, "pixels.txt")

# Vecindario

seg.setParameter(imagen)
seg.similitud(100)
