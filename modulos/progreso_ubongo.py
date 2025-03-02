import pickle

class ProgresoUbongo:
    def __init__(self, nivel=1, puntaje=0):
        self.nivel = nivel
        self.puntaje = puntaje

    def __repr__(self):
        return f"ProgresoUbongo(Nivel: {self.nivel}, Puntaje: {self.puntaje})"

    def guardar_progreso(self, archivo="progreso.pkl"):
        """Guarda el progreso en un archivo."""
        with open(archivo, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def cargar_progreso(archivo="progreso.pkl"):
        """Carga el progreso desde un archivo."""
        try:
            with open(archivo, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return ProgresoUbongo()  # Si no hay archivo, empezar desde 0
