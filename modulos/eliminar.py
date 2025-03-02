with open("modulos/ubongo_gui.py", "rb") as file:
    content = file.read()

clean_content = content.replace(b"\x00", b"")

with open("modulos/ubongo_gui.py", "wb") as file:
    file.write(clean_content)

print("Archivo limpiado con éxito.")
