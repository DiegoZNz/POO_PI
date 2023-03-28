import tkinter as tk
from tkinter import ttk
from tkinter import *
from ControladorBD import * #1. Presentamos los archivos XD

#2. Crear un objeto de la clase controiador 
controlador = ControladorBD()   #Nombre del objeto con la clase+

#3. Botonnnn
def EjecutaInsert():
    controlador.guardarUsuario(varNom.get(),varCor.get(),varCon.get())


Ventana= Tk()
Ventana.title("CRUD de Usuarios")
Ventana.geometry("500x400")

panel=ttk.Notebook (Ventana)
panel.pack(fill='both', expand='yes')
pestana1=ttk.Frame (panel)
pestana2=ttk.Frame (panel)
pestana3=ttk.Frame (panel)
pestana4=ttk. Frame(panel)


# Pestaña 1: Formulario de Usuarios 

titulo = Label(pestana1, text="Registro de usuarios", fg="blue", font="modern")
titulo.pack()

varId = tk.StringVar()
lblId = Label(pestana1, text="ID: ")
lblId.pack()
txtId = Entry(pestana1, textvariable=varId)
txtId.pack()

varNom = tk.StringVar()
lblNom = Label(pestana1, text="Nombre: ")
lblNom.pack()
txtNom = Entry(pestana1, textvariable=varNom)
txtNom.pack()

varApPat = tk.StringVar()
lblApPat = Label(pestana1, text="Apellido Paterno: ")
lblApPat.pack()
txtApPat = Entry(pestana1, textvariable=varApPat)
txtApPat.pack()

varApMat = tk.StringVar()
lblApMat = Label(pestana1, text="Apellido Materno: ")
lblApMat.pack()
txtApMat = Entry(pestana1, textvariable=varApMat)
txtApMat.pack()

varCor = tk.StringVar()
lblCor = Label(pestana1, text="Correo: ")
lblCor.pack()
txtCor = Entry(pestana1, textvariable=varCor)
txtCor.pack()

varOcup = tk.StringVar()
lblOcup = Label(pestana1, text="Ocupación: ")
lblOcup.pack()
txtOcup = Entry(pestana1, textvariable=varOcup)
txtOcup.pack()

btnGuardar = Button(pestana1, text='Guardar Usuario', command=EjecutaInsert)
btnGuardar.pack()

panel.add (pestana1, text='Alta usuarios')



Ventana.mainloop()
