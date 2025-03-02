import json
import os

class Usuario:
    def __init__(self, nombre, progreso=None, estadisticas=None):
        self.nombre = nombre
        self.progreso = progreso if progreso else {}
        self.estadisticas = estadisticas if estadisticas else {"partidas_jugadas": 0, "puntos": 0}
    
    def actualizar_puntuacion(self, puntos):
        self.estadisticas["puntos"] += puntos
        self.estadisticas["partidas_jugadas"] += 1
    
    def to_dict(self):
        return {"nombre": self.nombre, "progreso": self.progreso, "estadisticas": self.estadisticas}
    
    @staticmethod
    def from_dict(data):
        return Usuario(data["nombre"], data.get("progreso"), data.get("estadisticas"))