from tkinter import Tk
from modules import storage
from ui.login import ventana_login

def main():
    # Inicializar sistema
    storage.crear_directorios()
    storage.cargar_datos()
    
    # Asegurar que existe admin por defecto
    if not any(u["tipo"] == "admin" for u in storage.usuarios):
        storage.usuarios.append({
            "usuario": "admin",
            "contraseña": "admin123",
            "tipo": "admin"
        })
        storage.guardar_datos()
    
    # Iniciar aplicación
    ventana_login()

if __name__ == "__main__":
    main()