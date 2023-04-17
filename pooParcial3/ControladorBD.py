from tkinter import messagebox
import sqlite3
import bcrypt
import datetime

class ControladorBD:
    
    def __init__(self):
        pass
    
    #Metodos para crear conexiones
    def conexionBD(self):
        try:
            conexion= sqlite3.connect("C:/Users/diego/Documents/GitHub/POO_PI/pooParcial3/DBClientes.db")
            return conexion
        except sqlite3.OperationalError:
            print("No se pudo conectar a la base de datos")
            
    
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
    
    
    def MostrarClientes(self):
        conx=self.conexionBD()
        try:
            cursor=conx.cursor()
            clQuery = "SELECT IdCl, Nombre, APP, APM, Correo, Ocupacion FROM TBClientes"
            cursor.execute(clQuery)
            ResultQ = cursor.fetchall()
            conx.close()

            #5. retornar resultados en un while
            resultados = []
            for row in ResultQ:
                resultados.append(row)
            return resultados
        except sqlite3.OperationalError:
            print("error consulta")
            conx.close()
            
    def MostrarPedidos(self):
        conx=self.conexionBD()
        try:
            cursor=conx.cursor()
            clQuery = "SELECT TBPedidos.Id, TBPedidos.Fecha,  TBPedidos.Estado,TBPedidos.Total, TBClientes.Nombre FROM TBPedidos INNER JOIN TBClientes ON TBPedidos.IdCl = TBClientes.IdCl WHERE TBPedidos.Estado = 'Pendiente'"
            cursor.execute(clQuery)
            ResultQ = cursor.fetchall()
            conx.close()

            #5. retornar resultados en un while
            resultados = []
            for row in ResultQ:
                resultados.append(row)
            return resultados
        except sqlite3.OperationalError:
            print("error consulta")
            conx.close()
        
        
    ##################################################################### Metodos para usuarios ######################################################
    
    #validada al 100
    def guardarUsuario(self, Iden, nom, app, apm, cor, con, oc):
        conx = self.conexionBD()
        if (Iden == "" or nom == "" or app == "" or apm == "" or cor == "" or con == "" or oc == ""):
            messagebox.showwarning("Error", "Formulario incompleto")
            conx.close()
            return False
        else:
            try:
                int(Iden)
                # Encriptar la contraseña del usuario
                conH = self.encriptarCon(con)
                
                # Verificar si el usuario ya existe en la base de datos
                cursor = conx.cursor()
                cursor.execute("SELECT * FROM TBClientes WHERE IdCl=?", (Iden,))
                usuario_existente = cursor.fetchone()
                if usuario_existente is not None:
                    messagebox.showwarning("Error", f"El usuario {Iden} ya existe")
                    conx.close()
                    return False
                else:
                    # Insertar el nuevo usuario en la base de datos
                    datos = (Iden, nom, app, apm, cor, conH, oc)
                    qrInsert = "INSERT INTO TBClientes (IdCl, Nombre, APP, APM, Correo, Contraseña, Ocupacion) VALUES (?,?,?,?,?,?,?)"
                    cursor.execute(qrInsert, datos)
                    conx.commit()
                    conx.close()
                    messagebox.showinfo("Exito", "Usuario Guardado")
                    return True
            except ValueError:
                messagebox.showwarning("Error", "Tu Id no puede contener letras.")
            
    def encriptarCon(self, contra):
        ConPlana= contra
        ConPlana = ConPlana.encode()
        sal= bcrypt.gensalt()
        conHa = bcrypt.hashpw(ConPlana,sal)
        return conHa
    
    
    def LogIn(self, id, con):
        conx=self.conexionBD()
        if(id=="" or con==""):
            messagebox.showwarning("Error","Formulario incompleto")
            conx.close()
        else:
            try:
                int(id)
                cursor=conx.cursor()
                # Consulta para verificar si el usuario existe
                userQuery = "SELECT COUNT(*) FROM TBClientes WHERE IdCl=?"
                cursor.execute(userQuery, (id,))
                userCount = cursor.fetchone()[0]
                if userCount == 0:
                    messagebox.showerror("Error","El usuario no existe")
                    conx.close()
                    return False
                # Consulta para obtener la contraseña encriptada
                passQuery = "SELECT Contraseña FROM TBClientes WHERE IdCl=?"
                cursor.execute(passQuery, (id,))
                conEncriptada = cursor.fetchone()[0]
                if self.validarCon(con, conEncriptada):
                    messagebox.showinfo("Bienvenido","Vamos a comprar")
                    conx.close()
                    return True
                else:
                    messagebox.showerror("Error","Contraseña incorrecta")
                    conx.close()
                    return False
            except ValueError:
                messagebox.showwarning("Error", "Tu Id no puede contener letras.")

            
    def validarCon(self, ContraInput, ContraDataBase):
        ContraInput = ContraInput.encode()  # codificar la contraseña ingresada
        return bcrypt.checkpw(ContraInput, ContraDataBase)

    
    def ProdClient(self):
        conx=self.conexionBD()
        try:
            cursor=conx.cursor()
            prodQuery = "SELECT Id, Nombre, Descripcion, Precio, Categoria FROM TBProducto WHERE Disponibilidad='Sí'"
            cursor.execute(prodQuery)
            ResultQ = cursor.fetchall()
            conx.close()

            #5. retornar resultados en un while
            resultados = []
            for row in ResultQ:
                resultados.append(row)
            return resultados
        except sqlite3.OperationalError:
            print("error consulta")
            conx.close()
    
    
    def Pedidos(self,fecha, cliente, tot):
        conx=self.conexionBD()
        if tot==0:
            messagebox.showwarning("Error","Favor de seleccionar al menos un producto")
            conx.close()
        else: 
            confirmar = messagebox.askyesno("Realizar pedido", "¿Está seguro que desea pedir estos productos? No se podrá modificar despúes, asegurate que estan correctamente elegidos")
            if confirmar==True:
                try:
                    cursor=conx.cursor()
                    estado="Pendiente"
                    datos = (fecha, cliente,tot,estado)
                    pedidosQuery = "INSERT INTO TBPedidos (Fecha,IdCl,Total,Estado) VALUES (?,?,?,?)"
                    cursor.execute(pedidosQuery, datos)
                    conx.commit()
                    conx.close()
                    messagebox.showinfo("Exito", "Tu pedido ha sido realizado correctamente")
                    return True
                except sqlite3.OperationalError:
                    print("error consulta")
                    conx.close()
            else:
                messagebox.showerror("Error", "No se pudo realizar el pedido.")
                conx.close
                return False
            
            
    def PedClientes(self,cliente):
        conx=self.conexionBD()
        try:
            cursor=conx.cursor()
            prodQuery = "SELECT Id, Fecha, Total, Estado FROM TBPedidos WHERE IdCl="+cliente
            cursor.execute(prodQuery)
            ResultQ = cursor.fetchall()
            conx.close()

            #5. retornar resultados en un while
            resultados = []
            for row in ResultQ:
                resultados.append(row)
            return resultados
        except sqlite3.OperationalError:
            print("error consulta")
            conx.close()
            
    
                
        
            
            
    
    
    
    


        
        
    
    
    
    

            