import tkinter as tk
from modulos.ubongo_gui import Ubongo_GUI


if __name__ == "__main__":
    root = tk.Tk()
    juego = Ubongo_GUI(root)
    root.mainloop()
    
def limpiar_archivo(ruta):
    with open(ruta, 'rb') as f:
        contenido = f.read()

    # Reemplazar bytes nulos
    contenido_limpio = contenido.replace(b'\x00', b'')

    with open(ruta, 'wb') as f:
        f.write(contenido_limpio)

# Aplica la limpieza
limpiar_archivo("main.py")
limpiar_archivo("modulos/ubongo_gui.py")

print("Archivos limpiados exitosamente.")
