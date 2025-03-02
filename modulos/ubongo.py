from modulos.usuario import Usuario
from modulos.persistencia import Persistencia

class Ubongo:
    def __init__(self):
        self.usuarios = {}
        self.partidas = {}
        self.puntuaciones = {}
        self.cargar_datos()

    def crear_perfil(self, nombre):
        if nombre not in self.usuarios:
            self.usuarios[nombre] = Usuario(nombre)
            self.guardar_datos()

    def guardar_partida(self, nombre, partida):
        if nombre in self.usuarios:
            self.partidas[nombre] = partida
            self.guardar_datos()

    def cargar_partida(self, nombre):
        return self.partidas.get(nombre, None)
    
    def actualizar_puntuacion(self, nombre, puntos):
        if nombre in self.usuarios:
            self.usuarios[nombre].actualizar_puntuacion(puntos)
            self.registrar_puntuacion(nombre, puntos)
            self.guardar_datos()

    def guardar_datos(self):
        Persistencia.guardar_datos("config/datos.json", {
            "usuarios": {k: v.to_dict() for k, v in self.usuarios.items()},
            "partidas": self.partidas,
            "puntuaciones": self.puntuaciones
        })
    
    def cargar_datos(self):
        datos = Persistencia.cargar_datos("config/datos.json")
        self.usuarios = {k: Usuario.from_dict(v) for k, v in datos.get("usuarios", {}).items()}
        self.partidas = datos.get("partidas", {})
        self.puntuaciones = datos.get("puntuaciones", {})

    def registrar_puntuacion(self, nombre, puntuacion):
        if nombre not in self.puntuaciones:
            self.puntuaciones[nombre] = []
        self.puntuaciones[nombre].append(puntuacion)
        self.puntuaciones[nombre].sort(reverse=True)
        self.guardar_datos()

    def obtener_mejores_puntuaciones(self, top_n=10):
        return sorted([(nombre, max(puntos)) for nombre, puntos in self.puntuaciones.items() if puntos], key=lambda x: x[1], reverse=True)[:top_n]