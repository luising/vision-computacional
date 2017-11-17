from Imagen import *
import numpy as np

def Similitud(imagen):
    umbral = 50
    neighbor = 1
    pixels = np.array(imagen.pixels)
    neighbors = np.zeros(shape=imagen.size())
    mapp = np.zeros(shape=imagen.size())
    mapp[0, 0] = 2
    mapp[1, 1] = 1
    isfirst = 1
    row, column = imagen.size()
    while(not (mapp == -1).all()):
        if isfirst:
            isfirst = 0
        else:
            li = np.array(np.where(mapp == 0))
            l = li[li > 0]
            print("d->", l)
            ny, nx = li[li > 0][0]
            print(ny, nx)
            mapp[ny, nx] = 1
        while(not (mapp != 1).all()):
            try:
                activos = [np.where(mapp == 1)]
                for y, x in activos:
                    x = x[0]
                    y = y[0]
                    if x > 0 and y > 0 and y < row-2 and x < column-2:
                        n = x + 1
                        m = y + 1
                        h = np.abs(pixels[y - 1:y + 2,n - 1:n + 2] - pixels[y - 1:y + 2,x - 1:x + 2])
                        v = np.abs(pixels[m - 1:m + 2,x - 1:x + 2] - pixels[y - 1:y + 2,x - 1:x + 2])
                        r = h + v
                        fi = mr = mapp[y - 1:y + 2,x - 1:x + 2]
                        if(y - 1 == 0):
                            mr[0, :] = 2
                        if(x - 1 == 0):
                            mr[:, 0] = 2
                        if(x + 1 == column - 2):
                            mr[:, 2] = 2
                        if(y + 1 == row - 2):
                            mr[2, :] = 2
                        # print("actual\n", mr)
                        mr[(r < umbral) & (mr == 0)] = 1
                        mapp[y - 1:y + 2,x - 1:x + 2] = mr
                        mapp[y, x] = 2
                        # print("new\n", mapp[y - 1:y + 2,x - 1:x + 2])
            except Exception as e:
                print(e)
                print(row, column)
                print(y, x)
                print("inicio\n", fi)
                print("new\n", mapp[y - 1:y + 2,x - 1:x + 2])
                neighbors[np.where(mapp == 2)] = 255
                cv2.imwrite("bordes.png", neighbors)
                return
        print("vecindario encontrado", len(neighbors[np.where(mapp == 2)]))
        neighbors[np.where(mapp == 2)] = neighbor
        neighbor += 1
        mapp[np.where(mapp == 2)] = -1
    lm.saveMatriz(mapp, "borde.txt")
    lm.saveMatriz(neighbors, "v.txt")

Similitud(Imagen("p.png", 'L'))
