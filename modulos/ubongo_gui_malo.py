import tkinter as tk
from pathlib import Path
import time

class Ubongo_GUI:
    def __init__(self, root):
        self.root = root
        self.nivel_actual = 0  # Inicializa como 0
        self.cargar_niveles()  # Carga los niveles disponibles
        self.root.title("Ubongo - Juego de Rompecabezas")

        # Canvas para el tablero
        self.canvas = tk.Canvas(root, width=400, height=300, bg="black")
        self.canvas.pack()

        # Instrucciones
        self.instrucciones = tk.Label(root, text="Instrucciones:\n"
                                                  "1. Selecciona una pieza.\n"
                                                  "2. Coloca la pieza en la posición deseada.\n"
                                                  "3. Puedes rotar o voltear la pieza antes de colocarla.\n"
                                                  "4. Para quitar una pieza, haz clic en ella.\n"
                                                  "5. Completa el rompecabezas para ganar.", justify=tk.LEFT)
        self.instrucciones.pack(pady=10)

        # Botones de la interfaz
        self.btn_seleccionar_nivel = tk.Button(root, text="Seleccionar Nivel", command=self.abrir_menu_niveles)
        self.btn_seleccionar_nivel.pack(pady=3)
        
        self.btn_seleccionar_pieza = tk.Button(root, text="Seleccionar Pieza", command=self.abrir_menu_piezas, state=tk.DISABLED)
        self.btn_seleccionar_pieza.pack(pady=3)

        self.btn_rotar = tk.Button(root, text="Rotar", command=self.rotar_pieza, state=tk.DISABLED)
        self.btn_rotar.pack(pady=3)

        self.btn_voltear = tk.Button(root, text="Voltear", command=self.voltear_pieza, state=tk.DISABLED)
        self.btn_voltear.pack(pady=3)

        self.btn_colocar = tk.Button(root, text="Colocar", command=self.colocar_pieza, state=tk.DISABLED)
        self.btn_colocar.pack(pady=3)

        self.btn_quitar = tk.Button(root, text="Quitar Pieza", command=self.quitar_pieza, state=tk.DISABLED)
        self.btn_quitar.pack(pady=3)

        self.btn_historial = tk.Button(root, text="Ver Historial", command=self.mostrar_historial)
        self.btn_historial.pack(pady=3)

        self.btn_reiniciar = tk.Button(root, text="Reiniciar", command=self.reiniciar_juego)
        self.btn_reiniciar.pack(pady=3)

        self.btn_guardar = tk.Button(root, text="Guardar Partida", command=self.guardar_partida)
        self.btn_guardar.pack(pady=3)

        self.btn_cargar = tk.Button(root, text="Cargar Partida", command=self.cargar_partida)
        self.btn_cargar.pack(pady=3)

        self.btn_salir = tk.Button(root, text="Salir", command=self.root.quit)
        self.btn_salir.pack(pady=3)

        # Etiqueta de puntuación
        self.etiqueta_puntuacion = tk.Label(root, text="Puntuación: 0")
        self.etiqueta_puntuacion.pack(pady=5)

        # Variables del juego
        self.lista_niveles = [0,0]
        self.nivel_actual = 0
        self.piezas = [0,0]
        self.pieza_seleccionada = 0
        self.tablero = [0,0]
        self.historial_movimientos = [0,0]
        self.puntuacion = 0
        self.tiempo_inicio = 0
        self.posicion_pieza = [0, 0]  # Posición inicial de la pieza seleccionada

        # Eventos del mouse
        self.canvas.bind("<Button-1>", self.iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self.arrastrar_pieza)
        self.canvas.bind("<ButtonRelease-1>", self.soltar_pieza)

        # Cargar niveles disponibles
        self.cargar_niveles()

    def log_accion(self, mensaje):
        """Registra una acción en el historial."""
        self.historial_movimientos.append(mensaje)
        print(mensaje)

    def abrir_menu_niveles(self):
        """Abre una ventana para seleccionar un nivel."""
        ventana_niveles = tk.Toplevel(self.root)
        ventana_niveles.title("Seleccionar Nivel")

        for nivel in self.lista_niveles:
            btn_nivel = tk.Button(ventana_niveles, text=nivel.name, command=lambda n=nivel: self.cargar_nivel(n))
            btn_nivel.pack(pady=2)

    def abrir_menu_piezas(self):
        """Abre una ventana para seleccionar una pieza."""
        if not self.piezas:
            return

        ventana_piezas = tk.Toplevel(self.root)
        ventana_piezas.title("Seleccionar Pieza")

        for i, pieza in enumerate(self.piezas):
            btn_pieza = tk.Button(ventana_piezas, text=f"Pieza {i+1}", command=lambda p=i: self.seleccionar_pieza(p))
            btn_pieza.pack(pady=2)

    def seleccionar_pieza(self, indice):
        """Selecciona una pieza para colocar en el tablero."""
        self.pieza_seleccionada = indice
        self.btn_colocar.config(state=tk.NORMAL)
        self.btn_rotar.config(state=tk.NORMAL)
        self.btn_voltear.config(state=tk.NORMAL)
        self.btn_quitar.config(state=tk.NORMAL)
        self.mostrar_pieza()
        self.log_accion(f"Pieza {indice+1} seleccionada")

    def rotar_pieza(self):
        """Rota la pieza seleccionada."""
        if self.pieza_seleccionada is not 0:
            self.piezas[self.pieza_seleccionada] = list(zip(*self.piezas[self.pieza_seleccionada][::-1]))
            self.mostrar_tablero()
            self.mostrar_pieza()
            self.log_accion(f"Pieza {self.pieza_seleccionada+1} rotada")

    def voltear_pieza(self):
        """Voltea la pieza seleccionada."""
        if self.pieza_seleccionada is not 0:
            self.piezas[self.pieza_seleccionada] = [fila[::-1] for fila in self.piezas[self.pieza_seleccionada]]
            self.mostrar_tablero()
            self.mostrar_pieza()
            self.log_accion(f"Pieza {self.pieza_seleccionada+1} volteada")

    def colocar_pieza(self):
        """Coloca la pieza seleccionada en el tablero."""
        if self.pieza_seleccionada is not 0:
            pieza = self.piezas[self.pieza_seleccionada]
            if self.verificar_colocacion():
                for i, fila in enumerate(pieza):
                    for j, celda in enumerate(fila):
                        if celda:
                            self.tablero[i + self.posicion_pieza[1]][j + self.posicion_pieza[0]] = 1
                self.log_accion(f"Pieza {self.pieza_seleccionada+1} colocada en el tablero")
                self.pieza_seleccionada = 0
                self.btn_colocar.config(state=tk.DISABLED)
                self.mostrar_tablero()
                self.actualizar_puntuacion()
                self.verificar_victoria()
            else:
                self.mostrar_mensaje_error("La pieza no encaja en la posición seleccionada.")

    def quitar_pieza(self):
        """Quita la pieza seleccionada del tablero."""
        if self.pieza_seleccionada is not 0:
            pieza = self.piezas[self.pieza_seleccionada]
            for i, fila in enumerate(pieza):
                for j, celda in enumerate(fila):
                    if celda:
                        self.tablero[i + self.posicion_pieza[1]][j + self.posicion_pieza[0]] = 0
            self.log_accion(f"Pieza {self.pieza_seleccionada+1} quitada del tablero")
            self.pieza_seleccionada = 0
            self.btn_quitar.config(state=tk.DISABLED)
            self.mostrar_tablero()

    def mostrar_mensaje_error(self, mensaje):
        """Muestra un mensaje de error al usuario."""
        error_ventana = tk.Toplevel(self.root)
        error_ventana.title("Error")
        tk.Label(error_ventana, text=mensaje).pack(pady=10)
        tk.Button(error_ventana, text="Aceptar", command=error_ventana.destroy).pack(pady=5)

    def verificar_victoria(self):
        """Verifica si el rompecabezas está completo."""
        if all(all(celda == 1 for celda in fila) for fila in self.tablero):
            self.mostrar_mensaje_victoria()

    def mostrar_mensaje_victoria(self):
        """Muestra un mensaje de victoria al usuario."""
        victoria_ventana = tk.Toplevel(self.root)
        victoria_ventana.title("Victoria")
        tk.Label(victoria_ventana, text="¡Felicidades! Has completado el rompecabezas.").pack(pady=10)
        tk.Button(victoria_ventana, text="Aceptar", command=victoria_ventana.destroy).pack(pady=5)

    def verificar_colocacion(self):
        """Verifica si la pieza puede ser colocada en la posición actual."""
        pieza = self.piezas[self.pieza_seleccionada]
        for i, fila in enumerate(pieza):
            for j, celda in enumerate(fila):
                if celda:
                    if (i + self.posicion_pieza[1] >= len(self.tablero) or
                        j + self.posicion_pieza[0] >= len(self.tablero[0]) or
                        self.tablero[i + self.posicion_pieza[1]][j + self.posicion_pieza[0]] != 0):
                        return False
        return True

    def mostrar_tablero(self):
        """Dibuja el tablero en el canvas."""
        self.canvas.delete("all")
        for i, fila in enumerate(self.tablero):
            for j, celda in enumerate(fila):
                color = "black" if celda == 1 else "white"
                self.canvas.create_rectangle(j * 40, i * 40, j * 40 + 40, i * 40 + 40, fill=color)

    def mostrar_pieza(self):
        """Muestra la pieza seleccionada en el canvas."""
        if self.pieza_seleccionada is not 0:
            pieza = self.piezas[self.pieza_seleccionada]
            for i, fila in enumerate(pieza):
                for j, celda in enumerate(fila):
                    if celda:
                        x = (j + self.posicion_pieza[0]) * 40
                        y = (i + self.posicion_pieza[1]) * 40
                        self.canvas.create_rectangle(x, y, x+40, y+40, fill="blue", outline="gray", stipple="gray50")

    def cargar_niveles(self):
        """Carga los niveles disponibles desde la carpeta especificada."""
        carpeta_niveles = Path("niveles")
        if not carpeta_niveles.exists():
            self.log_accion("No se encontró la carpeta de niveles.")
            return

        self.lista_niveles = sorted(carpeta_niveles.glob("nivel_*.txt"))

        if not self.lista_niveles:
            self.log_accion("No se encontraron archivos de nivel.")
            return

        self.cargar_nivel(self.lista_niveles[0])

    def cargar_nivel(self, nivel_seleccionado):
        """Carga un nivel específico."""
        if nivel_seleccionado is 0:
            raise ValueError("No se ha seleccionado ningún nivel.")
        self.nivel_actual = Path(nivel_seleccionado)
        self.tablero, self.piezas = self.leer_nivel(self.nivel_actual)
        self.pieza_seleccionada = 0
        self.btn_seleccionar_pieza.config(state=tk.NORMAL)
        self.mostrar_tablero()
        self.iniciar_temporizador()
        self.log_accion(f"Nivel {nivel_seleccionado.name} cargado")

    def leer_nivel(self, ruta_archivo):
        """Lee un archivo de nivel y devuelve el tablero y las piezas."""
        try:
            with open(ruta_archivo, "r") as archivo:
                lineas = [linea.strip() for linea in archivo if linea.strip() and not linea.startswith("#")]

            filas, columnas = map(int, lineas[0].split())
            tablero = [list(map(int, linea.split())) for linea in lineas[1:filas+1]]

            num_piezas = int(lineas[filas+1])
            piezas = []
            indice = filas + 2

            for _ in range(num_piezas):
                filas_p, columnas_p = map(int, lineas[indice].split())
                pieza = [list(map(int, linea.split())) for linea in lineas[indice+1:indice+1+filas_p]]
                piezas.append(pieza)
                indice += 1 + filas_p

            return tablero, piezas
        except Exception as e:
            self.log_accion(f"Error al leer el archivo de nivel: {e}")
            return [], []

    def reiniciar_juego(self):
        """Reinicia el juego cargando el nivel actual nuevamente."""
        if self.nivel_actual is 0:
            self.log_accion("No hay ningún nivel cargado para reiniciar.")
            return
        self.cargar_nivel(self.nivel_actual)
        self.log_accion("Juego reiniciado")

    def iniciar_temporizador(self):
        """Inicia el temporizador para calcular la puntuación."""
        self.tiempo_inicio = time.time()

    def actualizar_puntuacion(self):
        """Actualiza la puntuación basada en el tiempo transcurrido."""
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        self.puntuacion = max(0, int(1000 / tiempo_transcurrido))
        self.etiqueta_puntuacion.config(text=f"Puntuación: {self.puntuacion}")

    def guardar_partida(self):
        """Guarda el estado actual del juego en un archivo."""
        try:
            with open("partida_guardada.txt", "w") as archivo:
                archivo.write(f"{self.nivel_actual}\n")
                archivo.write(f"{self.puntuacion}\n")
                archivo.write(f"{self.tiempo_inicio}\n")
                for fila in self.tablero:
                    archivo.write(" ".join(map(str, fila)) + "\n")
                for pieza in self.piezas:
                    archivo.write(f"{len(pieza)} {len(pieza[0])}\n")
                    for fila in pieza:
                        archivo.write(" ".join(map(str, fila)) + "\n")
            self.log_accion("Partida guardada")
        except Exception as e:
            self.log_accion(f"Error al guardar la partida: {e}")

    def cargar_partida(self):
        """Carga una partida guardada desde un archivo."""
        try:
            with open("partida_guardada.txt", "r") as archivo:
                lineas = archivo.readlines()
                self.nivel_actual = Path(lineas[0].strip())
                self.puntuacion = int(lineas[1].strip())
                self.tiempo_inicio = float(lineas[2].strip())
                self.tablero = [list(map(int, linea.strip().split())) for linea in lineas[3:3+len(self.tablero)]]
                self.piezas = []
                indice = 3 + len(self.tablero)
                while indice < len(lineas):
                    filas_p, columnas_p = map(int, lineas[indice].strip().split())
                    pieza = [list(map(int, lineas[indice+i+1].strip().split())) for i in range(filas_p)]
                    self.piezas.append(pieza)
                    indice += 1 + filas_p
            self.mostrar_tablero()
            self.etiqueta_puntuacion.config(text=f"Puntuación: {self.puntuacion}")
            self.log_accion("Partida cargada")
        except FileNotFoundError:
            self.log_accion("No se encontró un archivo de partida guardada.")
        except Exception as e:
            self.log_accion(f"Error al cargar la partida: {e}")

    def iniciar_arrastre(self, event):
        """Inicia el arrastre de la pieza."""
        if self.pieza_seleccionada is not 0:
            self.posicion_pieza = [event.x // 40, event.y // 40]
            self.mostrar_pieza()

    def arrastrar_pieza(self, event):
        """Arrastra la pieza seleccionada."""
        if self.pieza_seleccionada is not 0:
            self.posicion_pieza = [event.x // 40, event.y // 40]
            self.mostrar_tablero()
            self.mostrar_pieza()

    def soltar_pieza(self, event):
        """Suelta la pieza seleccionada."""
        if self.pieza_seleccionada is not 0:
            self.posicion_pieza = [event.x // 40, event.y // 40]
            if self.verificar_colocacion():
                self.colocar_pieza()
            else:
                self.log_accion("No se puede colocar la pieza aquí")
            self.mostrar_tablero()
            self.mostrar_pieza()

    def mostrar_historial(self):
        """Muestra el historial de movimientos."""
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("Historial de Movimientos")
        historial_texto = tk.Text(ventana_historial, height=15, width=50)
        historial_texto.pack(pady=10)
        historial_texto.insert(tk.END, "\n".join(self.historial_movimientos))
        historial_texto.config(state=tk.DISABLED)