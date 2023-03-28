from tkinter import messagebox
import sqlite3
import bcrypt

class ControladorBD:
    
    def __init__(self):
        pass
    
    #Metodos para crear coexiones
    def conexionBD(self):
        try:
            conexion= sqlite3.connect("C:/Users/diego/Documents/GitHub/POO_PI/pooParcial3/DBClientes.db")
            print("conectado a la base de datos")
            return conexion
        except sqlite3.OperationalError:
            print("No se pudo conectar a la base de datos")
            
    #Metodo para guardar usuarios
    def guardarUsuario(self, Iden,nom,app,apm,cor,oc):
        #1. usamos una conexion 
        conx=self.conexionBD()
        
        #2. validar parametros Vacios
        
        if(Iden=="0" or nom=="" or app=="" or apm=="" or cor=="" or oc==""):
            messagebox.showwarning("Aguas","Formulario incompleto")
        else:
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            
            cursor= conx.cursor()
            datos=(Iden,nom,app,apm,cor,oc)
            qrInsert="insert into TBClientes (IdCl, Nombre, APP, APM, Correo, Ocupacion) values (?,?,?,?,?,?)" 
            
            #4.Ejecutamos el insert y cerramos la conexion
            cursor.execute(qrInsert,datos)           
            conx.commit()
            messagebox.showinfo("Exito","Usuario Guardado")
            