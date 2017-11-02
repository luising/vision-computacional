from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
from utils import *
from filtrosS import *


class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.buildUI()
        self.parent.config(menu=self.menubar)

    def buildUI(self):

        self.parent.title("operadores de imagen ")
        self.pack()

        self.menubar = Menu(root)

        self.filemenu = Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="Abrir", command=self.loadFile)
        self.filemenu.add_command(label="Guardar", command=saveAllChanges)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Salir", command=self.parent.quit)

        self.menubar.add_cascade(label="Archivo", menu=self.filemenu)

        self.filtersmenu = Menu(self.menubar, tearoff=0)

        self.filtersmenu.add_command(label="escala grises ", command=lambda: applyFilter("g"))
        self.filtersmenu.add_command(label="copiado  ", command=lambda: applyFilter("co"))
        self.filtersmenu.add_command(label="invertir  ", command=lambda: applyFilter("in"))
        self.filtersmenu.add_command(label="brillo  ", command=lambda: cargar_opciones("brillo"))
        self.filtersmenu.add_command(label="clarado ", command=lambda: cargar_opciones("clarado"))
        self.filtersmenu.add_command(label="alongar contraste  ", command=lambda: cargar_opciones("contraste"))
        self.filtersmenu.add_command(label="reducccion de contraste ", command=lambda: cargar_opciones("Rcontraste"))

        self.menubar.add_cascade(label="operadores  Basico ", menu=self.filtersmenu)

        self.filtersmenuadv = Menu(self.menubar, tearoff=0)

        self.filtersmenuadv.add_command(label="shifting  HORIZONTAL ", command=lambda: applyFilter("sfI"))
        self.filtersmenuadv.add_command(label="shifting  VERTICAL ", command=lambda: applyFilter("sfV"))
        self.filtersmenuadv.add_command(label="shifting  DIAGONAL ", command=lambda: applyFilter("sfD"))
        self.filtersmenuadv.add_command(label="filtro de media   ", command=lambda: applyFilter("mediana"))
        self.filtersmenuadv.add_command(label="filtro modal  ", command=lambda: applyFilter("modal"))
        self.filtersmenuadv.add_command(label="ruido sal y pimienta  ", command=lambda: applyFilter("sal"))

        self.menubar.add_cascade(label="filtros avanzado ", menu=self.filtersmenuadv)

        self.filtersmenuUm = Menu(self.menubar, tearoff=0)

        self.filtersmenuUm.add_command(label="umbral binario ", command=lambda: cargar_opciones("umbralb"))
        self.filtersmenuUm.add_command(label="umbral 3, 4, 8, 16 ", command=lambda: cargar_opciones("umbral"))
        self.filtersmenuUm.add_command(label="umbral adaptativo ", command=lambda: applyFilter("adaptativo"))
        self.filtersmenuUm.add_command(label="umbral Varianza ", command=lambda: applyFilter("varianza"))
        self.filtersmenuUm.add_command(label="umbral orden de rango  ", command=lambda: cargar_opciones("orango"))
        self.filtersmenuUm.add_command(label="umbral entropía  ", command=lambda: applyFilter("entro"))
        self.filtersmenuUm.add_command(label="umbral máxima probabilidad ", command=lambda: applyFilter("MaxProb"))
        self.filtersmenuUm.add_command(label="umbral valle global   ", command=lambda: applyFilter("vg"))
        self.menubar.add_cascade(label="Umbrales ", menu=self.filtersmenuUm)

        self.menubar.add_command(label="Restaurar", command=lambda: applyFilter("o"))

        canvasContainer = Frame(self.parent)
        canvasContainer.pack(side=TOP)
        self.canvas = Canvas(canvasContainer, width=50, height=50)
        self.canvas.pack(side=LEFT, padx=5, pady=15)
        self.edit_canvas = Canvas(canvasContainer, width=50, height=50)
        self.edit_canvas.pack(side=RIGHT, padx=5, pady=15)

        scaleContainer = Frame(self.parent)
        scaleContainer.pack(side=BOTTOM)
        # componentes de nivel
        self.w = Label(root, text="nivel")
        self.e = Entry(root)
        self.button = Button(root, text='Modificar', width=25)
        self.nivel = (self.w, self.e, self.button)

        # self.minThreshold = Scale(root, from_=0, to=255, orient=HORIZONTAL)
        # self.minThreshold.pack(side=LEFT)

        return

    def updateCanvas(self, i, original=False):
        i = Image.open(i)
        w, h = i.size
        self.editImage = ImageTk.PhotoImage(i)
        self.edit_canvas.configure(width=w, height=h)
        self.edit_canvas.create_image(w / 2, h / 2, image=self.editImage)
        if(original):
            self.canvasImage = self.editImage
            self.canvas.configure(width=w, height=h)
            self.canvas.create_image(w / 2, h / 2, image=self.canvasImage)
        return

    def loadFile(self):
        global image, lastImage
        filename = askopenfilename(filetypes=[
                                   ("JPEG", "*.jpg"),
                                   ("JPEG", "*.jpeg"),
                                   ("PNG", "*.png")])
        if(filename):
            try:
                image = filename
                lastImage = image
                self.updateCanvas(image, original=True)
            except:
                print("Error opening file or file does not exists")
                showerror("Open Source File", "Failed to read file\n'%s'" % filename)
        return

    def hide_me(self):
        for event in self.nivel:
            event.pack_forget()

    def on_me(self, operacion):
        i = 0
        cargar = [0, 0, 0]
        for event in self.nivel:
            event = Button(root, text='Modificar', width=25, command=lambda: botonNivel(operacion)) if(type(event) == Button) else event
            event = Label(root, text="nivel " + operacion) if (type(event) == Label) else event
            cargar[i] = event
            i += 1
        self.nivel = cargar
        for event in self.nivel:
            event.pack(side=LEFT)


def applyFilter(f):
    global image, lastImage, app
    app.hide_me()
    if(f == "o"):
        i = image
    else:
        i = "tmp.png"
        a, width, height, pixels, pixels2d = imageToPixelsL(lastImage)
        print(pixels)
        if(f == "co"):
            app.updateCanvas(image)
            return
        else:
            pixels = escala_grises(pixels) if(f == "g") else pixels
            pixels = invertir(pixels) if(f == "in") else pixels
            pixels = Sal_Pimienta(pixels2d, width, height) if(f == "sal") else pixels
            pixels = mediana(pixels2d, width, height) if(f == "mediana") else pixels
            pixels = modal(pixels2d, width, height) if(f == "modal") else pixels
            pixels = convolution2Dr(pixels2d) if(f == "conv") else pixels
            pixels = Varianza(pixels, image, width, height) if(f == "varianza") else pixels
            pixels = valle_global(pixels, image) if(f == "vg") else pixels
            pixels = entropia(pixels, image, width, height) if(f == "entro") else pixels
            pixels = adaptativo(pixels2d, image, width, height) if(f == "adaptativo") else pixels
            pixels = MaxProb(pixels, image) if(f == "MaxProb") else pixels
            pixels = shiftingI(pixels2d, width, height) if(f == "sfI") else pixels
            pixels = shiftingV(pixels2d, width, height) if(f == "sfV") else pixels
            pixels = shiftingD(pixels2d, width, height) if(f == "sfD") else pixels
        print("matriz nueva")
        print(pixels)
        saveImage((width, height), pixels, i)
    lastImage = i
    app.updateCanvas(i)
    print("Terminado!")
    return


def botonNivel(operacion):
    app.hide_me()
    Input = ""
    i = "tmp.png"
    global image, lastImage
    a, width, height, pixels, pixels2d = imageToPixelsL(lastImage)
    if operacion == "clarado" or "brillo" == operacion or "umbral" == operacion or "umbralb" == operacion:
        Input = int(app.e.get())
        pixels = clarado(pixels, Input) if("clarado" == operacion) else pixels
        pixels = brillo(pixels, Input) if("brillo" == operacion) else pixels
        pixels = umbralb(pixels, Input) if("umbralb" == operacion) else pixels
        pixels = umbral(pixels, Input) if("umbral" == operacion) else pixels
    elif operacion == "contraste" or operacion == "Rcontraste":
        Input = (app.e.get()).split(",")
        pixels = Acontraste(pixels, int(Input[0]), int(Input[1])) if("contraste" == operacion) else pixels
        pixels = Rcontraste(pixels, int(Input[0]), int(Input[1])) if("Rcontraste" == operacion) else pixels
        # if("orango" == operacion):
        #     width, height, pixels = obtenerRango(image, Input)
    saveImage((width, height), pixels, i)
    lastImage = i
    app.updateCanvas(i)


def cargar_opciones(operacion):
        app.on_me(operacion)


root = Tk()
app = App(root)
image, lastImage = None, None
root.mainloop()
