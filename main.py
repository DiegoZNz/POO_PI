import tkinter as tk
from tkinter import messagebox

class CafeteriaApp:
    def __init__(self, master):
        self.master = master
        master.title("Cafeteria App")

        # Crea los widgets para el menú
        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.menu_label = tk.Label(self.menu_frame, text="Menú")
        self.menu_label.pack()
        self.menu_listbox = tk.Listbox(self.menu_frame)
        self.menu_listbox.pack()
        self.menu_listbox.insert(tk.END, "Café con leche")
        self.menu_listbox.insert(tk.END, "Capuchino")
        self.menu_listbox.insert(tk.END, "Latte Macchiato")
        self.menu_listbox.insert(tk.END, "Té")
        self.menu_listbox.insert(tk.END, "Jugo")
        self.menu_listbox.insert(tk.END, "Pastel")
        self.menu_listbox.insert(tk.END, "Galleta")

        # Crea los widgets para el carrito
        self.cart_frame = tk.Frame(master)
        self.cart_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.cart_label = tk.Label(self.cart_frame, text="Carrito")
        self.cart_label.pack()
        self.cart_listbox = tk.Listbox(self.cart_frame)
        self.cart_listbox.pack()
        self.add_button = tk.Button(self.cart_frame, text="Agregar", command=self.add_to_cart)
        self.add_button.pack()
        self.remove_button = tk.Button(self.cart_frame, text="Eliminar", command=self.remove_from_cart)
        self.remove_button.pack()
        self.checkout_button = tk.Button(self.cart_frame, text="Pagar", command=self.checkout)
        self.checkout_button.pack()

    def add_to_cart(self):
        # Agrega el elemento seleccionado al carrito
        item = self.menu_listbox.get(tk.ACTIVE)
        self.cart_listbox.insert(tk.END, item)

    def remove_from_cart(self):
        # Elimina el elemento seleccionado del carrito
        index = self.cart_listbox.curselection()
        self.cart_listbox.delete(index)

    def checkout(self):
        # Muestra un mensaje de confirmación y vacía el carrito
        tk.messagebox.showinfo("Compra realizada", "¡Gracias por su compra!")
        self.cart_listbox.delete(0, tk.END)

root = tk.Tk()
app = CafeteriaApp(root)
root.mainloop()
