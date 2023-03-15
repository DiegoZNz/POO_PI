import tkinter as tk

class App:
    def __init__(self, master):
        self.master = master
        master.title("Cafetería")

        # Creamos la barra de menú
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        # Creamos el menú de productos
        productos_menu = tk.Menu(menubar, tearoff=0)
        productos_menu.add_command(label="Café", command=lambda: self.abrir_ventana_agregar("Café"))
        productos_menu.add_command(label="Té", command=lambda: self.abrir_ventana_agregar("Té"))
        productos_menu.add_command(label="Galletas", command=lambda: self.abrir_ventana_agregar("Galletas"))

        # Agregamos el menú de productos a la barra de menú
        menubar.add_cascade(label="Productos", menu=productos_menu)

        # Creamos etiquetas y entradas para mostrar y agregar productos
        self.productos_agregados_label = tk.Label(master, text="Productos agregados: ")
        self.productos_agregados_label.pack()

        self.productos_agregados = tk.Label(master, text="")
        self.productos_agregados.pack()

        self.ventana_agregar = None
        self.producto_a_agregar = None

    def abrir_ventana_agregar(self, producto):
        self.producto_a_agregar = producto
        self.ventana_agregar = tk.Toplevel(self.master)

        # Creamos etiquetas y entradas para agregar productos
        tk.Label(self.ventana_agregar, text=f"Cantidad de {producto}:").grid(row=0, column=0)
        self.cantidad_entry = tk.Entry(self.ventana_agregar)
        self.cantidad_entry.grid(row=0, column=1)

        tk.Button(self.ventana_agregar, text="Agregar", command=self.agregar_producto).grid(row=1, column=0)
        tk.Button(self.ventana_agregar, text="Cancelar", command=self.ventana_agregar.destroy).grid(row=1, column=1)

    def agregar_producto(self):
        cantidad = self.cantidad_entry.get()
        self.cantidad_entry.delete(0, tk.END)

        self.ventana_agregar.destroy()

        productos_agregados = self.productos_agregados.cget("text")

        if productos_agregados:
            productos_agregados += f", {cantidad} {self.producto_a_agregar}"
        else:
            productos_agregados = f"{cantidad} {self.producto_a_agregar}"

        self.productos_agregados.config(text=productos_agregados)

root = tk.Tk()
app = App(root)
root.mainloop()
