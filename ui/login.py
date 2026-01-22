from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Toplevel, StringVar, OptionMenu
from PIL import Image, ImageTk
import os
from modules import storage
from ui.admin import ventana_admin
from ui.coop import ventana_cooperativa
from ui.passenger import ventana_pasajero

def abrir_registro(root):
    nueva_ventana = Toplevel(root)
    nueva_ventana.title("Registro")
    nueva_ventana.geometry("400x400")

    Label(nueva_ventana, text="REGISTRAR NUEVO USUARIO", font=("Arial", 14, "bold")).pack(pady=10)
    frame_campos = Frame(nueva_ventana)
    frame_campos.pack(pady=10)

    Label(frame_campos, text="Nuevo usuario:").grid(row=0, column=0, pady=5, sticky="e")
    entry_user = Entry(frame_campos, width=25)
    entry_user.grid(row=0, column=1, pady=5)

    Label(frame_campos, text="Nueva contraseña:").grid(row=1, column=0, pady=5, sticky="e")
    entry_contra = Entry(frame_campos, show="*", width=25)
    entry_contra.grid(row=1, column=1, pady=5)

    Label(frame_campos, text="Tipo de usuario:").grid(row=2, column=0, pady=5, sticky="e")
    tipo_var = StringVar(nueva_ventana)
    tipo_var.set("pasajero")
    OptionMenu(frame_campos, tipo_var, "pasajero", "cooperativa", "admin").grid(row=2, column=1, pady=5)

    def guardar_usuario():
        nuevo_usuario = entry_user.get().strip()
        nueva_contra = entry_contra.get().strip()
        tipo = tipo_var.get()

        if not nuevo_usuario or not nueva_contra:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos")
            return

        for u in storage.usuarios:
            if u["usuario"] == nuevo_usuario:
                messagebox.showerror("Error", "Ese usuario ya existe")
                return

        storage.usuarios.append({
            "usuario": nuevo_usuario,
            "contraseña": nueva_contra,
            "tipo": tipo
        })
        storage.guardar_datos()
        messagebox.showinfo("Éxito", f"Usuario {tipo} registrado correctamente")
        nueva_ventana.destroy()

    frame_botones = Frame(nueva_ventana)
    frame_botones.pack(pady=20)
    Button(frame_botones, text="Guardar", command=guardar_usuario, width=15).pack(pady=5)
    Button(frame_botones, text="Cerrar", command=nueva_ventana.destroy, width=15).pack(pady=5)

def entrar(entry_user, entry_contra, root):
    nombre = entry_user.get().strip()
    contra = entry_contra.get().strip()

    if not nombre or not contra:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos")
        return

    for u in storage.usuarios:
        if u["usuario"] == nombre and u["contraseña"] == contra:
            messagebox.showinfo("Acceso correcto", f"Bienvenido {nombre}")
            root.destroy()
            
            if u["tipo"] == "admin":
                ventana_admin()
            elif u["tipo"] == "cooperativa":
                ventana_cooperativa(nombre)
            else:
                ventana_pasajero(nombre)
            return

    messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

def ventana_login():
    root = Tk()
    root.title("Sistema de Transporte - Login")
    root.geometry("500x500")

    frame_superior = Frame(root)
    frame_superior.pack(fill="both", expand=True)
    frame_inferior = Frame(root)
    frame_inferior.pack(fill="both", expand=True)
    
    Label(frame_superior, text="SISTEMA DE TRANSPORTE", font=("Arial", 16, "bold")).pack(pady=20)
    Label(frame_superior, text="Login", font=("Arial", 14)).pack(pady=10)
    
    # Intentar cargar logo con ruta segura
    try:
        logo_path = os.path.join("imagenes", "logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            render = ImageTk.PhotoImage(img)
            lbl_img = Label(frame_superior, image=render)
            lbl_img.image = render
            lbl_img.pack(pady=10)
    except Exception as e:
        pass # Ignorar si no hay logo

    frame_campos = Frame(frame_inferior)
    frame_campos.pack(pady=20)
    
    Label(frame_campos, text="Usuario:", font=("Arial", 10)).grid(row=0, column=0, pady=5, sticky="e")
    entry_user = Entry(frame_campos, width=25)
    entry_user.grid(row=0, column=1, pady=5, padx=10)
    
    Label(frame_campos, text="Contraseña:", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="e")
    entry_contra = Entry(frame_campos, show="*", width=25)
    entry_contra.grid(row=1, column=1, pady=5, padx=10)

    frame_botones = Frame(frame_inferior)
    frame_botones.pack(pady=20)
    
    Button(frame_botones, text="Ingresar",
           command=lambda: entrar(entry_user, entry_contra, root),
           width=15, height=2).pack(side="left", padx=10)
    
    Button(frame_botones, text="Registrar",
           command=lambda: abrir_registro(root),
           width=15, height=2).pack(side="left", padx=10)
    
    root.mainloop()