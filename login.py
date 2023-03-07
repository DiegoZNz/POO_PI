import tkinter as tk

# Definir el diccionario de usuarios y contraseñas
users = {"usuario1": "contraseña1", "usuario2": "contraseña2", "usuario3": "contraseña3"}

# Función para verificar el usuario y contraseña ingresados
def check_login():
    usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()
    if usuario in users and users[usuario] == contraseña:
        # Si el usuario y contraseña son válidos, cerrar la ventana de login
        login_window.destroy()
        # Aquí iría el código para mostrar el menú de la cafetería
    else:
        # Si el usuario y contraseña son inválidos, mostrar un mensaje de error
        error_label.config(text="Usuario o contraseña incorrectos")

# Crear la ventana de login
login_window = tk.Tk()
login_window.title("Login")

# Crear los widgets de la ventana de login
usuario_label = tk.Label(login_window, text="Usuario:")
usuario_entry = tk.Entry(login_window)
contraseña_label = tk.Label(login_window, text="Contraseña:")
contraseña_entry = tk.Entry(login_window, show="*")
login_button = tk.Button(login_window, text="Iniciar sesión", command=check_login)
error_label = tk.Label(login_window, text="", fg="red")

# Añadir los widgets a la ventana de login
usuario_label.pack()
usuario_entry.pack()
contraseña_label.pack()
contraseña_entry.pack()
login_button.pack()
error_label.pack()

# Ejecutar el bucle principal de la ventana de login
login_window.mainloop()