from tkinter import messagebox
import sqlite3

class ControladorBD:
    
    def __init__(self):
        pass
    
    #Metodos para crear coexiones
    def conexionBD(self):
        try:
            conexion= sqlite3.connect("C:/Users/diego/Documents/GitHub/POO_PI/pooParcial3/DBClientes.db")
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
            conx.close
        else:
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            
            cursor= conx.cursor()
            datos=(Iden,nom,app,apm,cor,oc)
            qrInsert="insert into TBClientes (IdCl, Nombre, APP, APM, Correo, Ocupacion) values (?,?,?,?,?,?)" 
            
            #4.Ejecutamos el insert y cerramos la conexion
            cursor.execute(qrInsert,datos)           
            conx.commit()
            conx.close
            messagebox.showinfo("Exito","Usuario Guardado")
            
    def guardarProducto(self, nom,desc,prec,cat,disp):
        #1. usamos una conexion 
        conx=self.conexionBD()
        
        #2. validar parámetros vacíos
        
        if(nom=="" or desc=="" or prec=="" or cat=="" or disp==""):
            messagebox.showwarning("Aguas","Formulario incompleto")
            conx.close
            return False
        #2. validar que la disponibilidad sea solo Sí o No, de lo coincide manda un mensaje que cheque ese apartado
        if disp not in ["Sí", "No"]:
            messagebox.showwarning("Error","El campo de disponibilidad solo admite sí o No, favor de seleccionar una opción válida")
            conx.close
            return False
        try:
            #por ultimo validamos que el precio sea un número flotante, si es así se ejecuta la consulta de agregar producto, de lo contrario manda error.
            float(prec)
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            cursor= conx.cursor()
            datos=(nom,desc,prec,cat,disp)
            qrInsert="insert into TBProducto (Nombre, Descripcion, Precio, Categoria, Disponibilidad) values (?,?,?,?,?)" 
            
            #4.Ejecutamos el insert y cerramos la conexion
            cursor.execute(qrInsert,datos)           
            conx.commit()
            conx.close
            messagebox.showinfo("Exito","Producto Guardado")
            return True
        except ValueError:
            messagebox.showwarning("Error", "El precio debe ser un NÚMERO válido.")
            conx.close
            return False

        
    def ConsultarProd(self):
        #1. usamos una conexion 
        conx=self.conexionBD()
        try:
            cursor=conx.cursor()
            selectquery = "SELECT * FROM TBProducto"

            #4.ejecuta y guarda la consulta
            cursor.execute(selectquery)
            rsProd = cursor.fetchall()
            conx.close()

            #5. retornar resultados en un while
            lista = []
            for row in rsProd:
                lista.append(row)
            return lista

        except sqlite3.OperationalError:
            print("error consulta")
            
        
    def ActualizarProducto(self, id,nom,desc,prec,cat,disp):
        #1. usamos una conexion 
        conx=self.conexionBD()
        
        #2. validar parámetros vacíos
        
        if(nom=="" or desc=="" or prec=="" or cat=="" or disp==""):
            messagebox.showwarning("Campos incompletos","No puedes actualzar un formulario y dejar campos vacíos")
            return False
        #2. validar que la disponibilidad sea solo Sí o No, de lo coincide manda un mensaje que cheque ese apartado
        if disp not in ["Sí", "No"]:
            messagebox.showwarning("Error","El campo de disponibilidad solo admite sí o No, favor de seleccionar una opción válida")
            return False
        try:
            #por ultimo validamos que el precio sea un número flotante, si es así se ejecuta la consulta de agregar producto, de lo contrario manda error.
            float(prec)
            #3. Preparamos el cursor, datos que voy a insertar y el querySQL
            cursor= conx.cursor()
            datosUP=(nom,desc,prec,cat,disp)
            qrUPD="UPDATE TBProducto SET Nombre=?, Descripcion=?, Precio=?, Categoria=?, Disponibilidad=? Where Id="+id
            #4.Ejecutamos el insert y cerramos la conexion
            cursor.execute(qrUPD,datosUP)           
            conx.commit()
            messagebox.showinfo("Exito","Producto Actualizado")
            return True
        except ValueError:
            messagebox.showwarning("Error", "El precio debe ser un NÚMERO válido.")
            return False

    
    def EliminarProducto(self,id):
        conx=self.conexionBD()
        #Preguntar si quiere eliminar 
        confirmar = messagebox.askyesno("Eliminar Producto", "¿Está seguro que desea eliminar este Producto? Ya no habrá punto de retorno")
        if confirmar==True:
            try:
                #3 cursos y query
                cursor=conx.cursor()
                DLTQR = "DELETE FROM TBProducto WHERE Id="+id
                #4.ejecuta y guarda la consulta
                cursor.execute(DLTQR)
                conx.commit()
                conx.close
                return True
            except sqlite3.OperationalError:
                print("error consulta")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el producto.")
            conx.close
            return False