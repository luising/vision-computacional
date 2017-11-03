
import cv2
import numpy as np
import sys
def CrearTxt(Matriz):
    lista = []
    name="Matriz.txt"
    file=open(name,'w') 
    for pixel in Matriz:
        for fila in pixel:

            file.write(str(fila)+ ",")
        file.write("\n")

    file.close() 
class Image(object):
    def __init__(self, nameImage, mode):
        self.mode = mode
        self.nameImage = nameImage
        self.ToPixels(mode)    
    def Cv2Save(self, path):
        cv2.imwrite(path, self.pixels)
    def ToPixels(self, mode="RGB"):
        if mode != "RGB":
            imagen = cv2.imread(self.nameImage, 0)
        self.pixels = imagen
        self.h, self.w = imagen.shape
        self.listpixels = list()
        for y in range(self.h):
            for x in range(self.w):
                self.listpixels.append(self.pixels[y, x])
    def ImageSize(self):
        return (self.h, self.w)
Intensity = 254
AssignedBeta = 180
imagen = Image("binAje.png", 'L')
height, width = imagen.ImageSize()

print(height, width)
Horizontal_Neighboor_2 = [[(abs(int(imagen.pixels[i][j + 1]) - int(imagen.pixels[i][j]))) for j in range(width - 1)] for i in range(height)]
Vertical_Neighboor_2 = [[(abs(int(imagen.pixels[i + 1][j]) - int(imagen.pixels[i][j]))) for j in range(width)] for i in range(height - 1)]

for i in range(height - 1):
    for j in range(width - 1):
        Horizontal_Neighbor = Horizontal_Neighboor_2[i][j]
        if Horizontal_Neighbor < AssignedBeta:
            imagen.pixels[i,j] = 255
            
        else:
            imagen.pixels[i, j] = 0
            
 

for j in range(0,width-1):
    for i in range(0,height-1):
        Vertical_Neighboor = Vertical_Neighboor_2[i][j]
        if Vertical_Neighboor > AssignedBeta:
            imagen.pixels[i, j] = 0
            
print ("Matriz procesada:")
for pixel in imagen.pixels:
        print(pixel)
imagen.Cv2Save("similitud.png")

CrearTxt(imagen.pixels)