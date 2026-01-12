from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Toplevel
from PIL import Image, ImageTk

usuarios = [] 


# Ventana de registro
def abrir_registro(root):
    nueva_ventana = Toplevel(root)
    nueva_ventana.title("Registro")

    Label(nueva_ventana, text="REGISTRAR USUARIO").pack(pady=10)

    Label(nueva_ventana, text="Nuevo usuario:").pack()
    entry_user = Entry(nueva_ventana)
    entry_user.pack()

    Label(nueva_ventana, text="Nueva contraseña:").pack()
    entry_contra = Entry(nueva_ventana, show="*")
    entry_contra.pack()

    def guardar_usuario():
        nuevo_usuario = entry_user.get().strip()
        nueva_contra = entry_contra.get().strip()

        if not nuevo_usuario or not nueva_contra:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos")
            return

        for u in usuarios:
            if u["usuario"] == nuevo_usuario:
                messagebox.showerror("Error", "Ese usuario ya existe")
                return

        usuarios.append({"usuario": nuevo_usuario, "contraseña": nueva_contra})
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        nueva_ventana.destroy()

    Button(nueva_ventana, text="Guardar", command=guardar_usuario).pack(pady=10)
    Button(nueva_ventana, text="Cerrar", command=nueva_ventana.destroy).pack()


# Función para ingresar
def entrar(entry_user, entry_contra):
    nombre = entry_user.get().strip()
    contra = entry_contra.get().strip()

    if not nombre or not contra:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos")
        return

    for u in usuarios:
        if u["usuario"] == nombre and u["contraseña"] == contra:
            messagebox.showinfo("Acceso correcto", f"Bienvenido {nombre}")
            return

    messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")


# Ventana principal de login
def ventana_login():
    root = Tk()
    root.title("Login")

    frame_superior = Frame(root)
    frame_superior.pack(fill="both", expand=True)
    frame_inferior = Frame(root)
    frame_inferior.pack(fill="both", expand=True)
    frame_inferior.columnconfigure(0, weight=1)
    frame_inferior.columnconfigure(1, weight=1)
    Label(frame_superior, text="Login").pack(pady=10)
    img = Image.open("imagenes/logo.png")
    render = ImageTk.PhotoImage(img)
    lbl_img = Label(frame_superior, image=render)
    lbl_img.image = render
    lbl_img.pack()

    # Usuario
    Label(frame_inferior, text="Usuario:").grid(row=0, column=0, sticky="e")
    entry_user = Entry(frame_inferior)
    entry_user.grid(row=0, column=1)

    # Contraseña
    Label(frame_inferior, text="Contraseña:").grid(row=1, column=0, sticky="e")
    entry_contra = Entry(frame_inferior, show="*")
    entry_contra.grid(row=1, column=1)

    # Botón ingresar
    Button(frame_inferior,
           text="Ingresar",
           command=lambda: entrar(entry_user, entry_contra)
           ).grid(row=2, column=0, columnspan=2, pady=10)

    # Botón registrar
    Button(frame_inferior,
           text="Registrar",
           command=lambda: abrir_registro(root)
           ).grid(row=3, column=0, columnspan=2, pady=5)

    root.mainloop()


ventana_login()