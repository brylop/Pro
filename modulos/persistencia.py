import json
import os

class Persistencia:
    @staticmethod
    def guardar_datos(archivo, datos):
        try:
            with open(archivo, "w") as f:
                json.dump(datos, f, indent=4)
        except Exception as e:
            print(f"Error al guardar datos: {e}")
    
    @staticmethod
    def cargar_datos(archivo):
        if os.path.exists(archivo):
            try:
                with open(archivo, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error al cargar datos: {e}")
        return {}