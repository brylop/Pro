# Ubongo - Juego de Rompecabezas

Ubongo es un juego de rompecabezas donde los jugadores deben colocar piezas en un tablero siguiendo ciertas reglas. Esta implementación en Python utiliza la biblioteca Tkinter para proporcionar una interfaz gráfica interactiva.

## Características

- Selección de niveles desde archivos predefinidos.
- Visualización del tablero y piezas disponibles.
- Rotación y volteo de piezas.
- Colocación de piezas en el tablero.
- Historial de movimientos.
- Reinicio del nivel.
- Validación de que la pieza encaje correctamente en la posición seleccionada.
- Mensajes de error cuando un movimiento no es válido.
- Posibilidad de quitar una ficha ya colocada.
- Modificación de la posición y orientación de una ficha ya colocada.
- Mensaje de victoria cuando se complete el rompecabezas.

## Requisitos

- Python 3.x
- Tkinter (incluido por defecto en la instalación de Python)

## Instalación y Ejecución

1. Clonar o descargar este repositorio.
2. Asegurarse de que la carpeta `niveles` contenga archivos de configuración de niveles.
3. Ejecutar el siguiente comando:
   ```bash
   python ubongo.py
   ```

## Estructura del Proyecto

- `ubongo.py`: Archivo principal que gestiona la interfaz y la lógica del juego.
- `niveles/`: Carpeta que contiene los archivos de configuración de niveles.
- `README.md`: Documento explicativo sobre el proyecto.

## Uso

1. Seleccionar un nivel.
2. Elegir una pieza.
3. Rotar, voltear y colocar la pieza en el tablero.
4. Quitar o modificar la posición de una pieza ya colocada.
5. Consultar el historial de movimientos si es necesario.
6. Reiniciar el nivel en caso de ser necesario.
7. Completar el rompecabezas para recibir el mensaje de victoria.

## Notas Adicionales

- Los niveles deben estar en la carpeta `niveles` y seguir un formato predefinido.
- El historial de movimientos se almacena en una ventana emergente accesible desde el botón correspondiente.
- El juego puede expandirse agregando nuevos niveles y piezas.

## Autor

Juan David Arenas Forero

